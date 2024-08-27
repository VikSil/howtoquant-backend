# global imports
import inspect
import logging
import os
import pandas as pd
import sys
from django_cron import CronJobBase, Schedule
from django.contrib.contenttypes.models import ContentType

# local imports

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  # add parent dir to path to import upstream modules

from .utils_queue import select_proc_flag_from_queue, set_processing_flag
from apps.accounting.models import trade, asset_flow, instrument_position, cash_position
from apps.classifiers.models import asset_flow_type
from howtoquant.utils import save_df_to_db

logger = logging.getLogger(__name__)


class FlowBooker(CronJobBase):

    FREQUENCY_IN_MINS = 1

    schedule = Schedule(run_every_mins=FREQUENCY_IN_MINS)
    code = 'config.flow_booker'

    def do(self):
        self.process_new_trades()
        self.process_new_positions()

    def process_cash_flow(self, trade_id, position_id):

        try:
            # filter for an existing object via the Generic Key
            trade_line = trade.objects.get(pk=trade_id)
            cash_line = cash_position.objects.filter(pk=position_id).first()
            flow_line = asset_flow.objects.filter(
                position_id=cash_line.id,
                position_type=ContentType.objects.get_for_model(cash_line).id,
                source_id=trade_line.id,
                source_type=ContentType.objects.get_for_model(trade_line).id,
            )
            if not flow_line:
                # new trade flow
                direction = 1
                if trade_line.bs_indicator == 'B':
                    direction = -1  # if buying then cash flows out

                new_asset_flow = asset_flow.objects.create(
                    position_fk=cash_line,
                    trade_date=trade_line.trade_datetime,
                    settlement_date=trade_line.settlement_date,
                    quantity=trade_line.gross_consideration * direction,
                    price=trade_line.price * trade_line.trade_settlement_xrate,
                    asset_flow_type=asset_flow_type.objects.get(type_name='Cash Flow'),
                    ccy=trade_line.settlement_ccy,
                    xrate=trade_line.settlement_base_xrate,
                    source_fk=trade_line,
                )
                new_asset_flow.save()

            else:
                # existing flow handling to be implemented with trade amendments
                pass

        except Exception as e:
            logger.debug(f'An error occured while processing settlement cash flow for trade: {trade_id}')
            return False

        return True

    def process_instrument_flow(self, trade_id, position_id):

        try:
            # filter for an existing object via the Generic Key
            trade_line = trade.objects.get(pk=trade_id)
            inst_line = instrument_position.objects.filter(pk=position_id).first()
            flow_line = asset_flow.objects.filter(
                position_id=inst_line.id,
                position_type=ContentType.objects.get_for_model(inst_line).id,
                source_id=trade_line.id,
                source_type=ContentType.objects.get_for_model(trade_line).id,
            )
            if not flow_line:
                # new trade flow
                direction = 1
                if trade_line.bs_indicator == 'S':
                    direction = -1

                new_asset_flow = asset_flow.objects.create(
                    position_fk=inst_line,
                    trade_date=trade_line.trade_datetime,
                    settlement_date=trade_line.settlement_date,
                    quantity=trade_line.quantity * direction,
                    price=trade_line.price,
                    asset_flow_type=asset_flow_type.objects.get(type_name='Instrument Flow'),
                    ccy=trade_line.ccy,
                    xrate=trade_line.trade_settlement_xrate * trade_line.settlement_base_xrate,
                    source_fk=trade_line,
                )
                new_asset_flow.save()

            else:
                # existing flow handling to be implemented with trade amendments
                pass

        except Exception as e:
            logger.debug(f'An error occured while processing instrument flow for trade: {trade_id}')
            return False

        return True

    def process_new_positions(self):
        queue_df = select_proc_flag_from_queue('FLOW_BOOKER', 'F')

        # process instrument flows
        flow_df = queue_df.drop(queue_df.columns.difference(['id', 'source_id', 'arg1', 'arg3']), axis=1)

        inst_pos_processing_results = [
            (row[0], self.process_instrument_flow(row[1], row[2]))
            for row in zip(
                flow_df['id'],
                flow_df['source_id'],
                flow_df['arg1'],
            )
        ]
        inst_pos_processing_results_df = pd.DataFrame(inst_pos_processing_results, columns=['msg_id', 'inst_result'])

        # process cash flows
        cash_pos_processing_results = [
            (row[0], self.process_cash_flow(row[1], row[2]))
            for row in zip(
                flow_df['id'],
                flow_df['source_id'],
                flow_df['arg3'],
            )
        ]
        cash_pos_processing_results_df = pd.DataFrame(cash_pos_processing_results, columns=['msg_id', 'cash_result'])

        # find sucessfully processed and failed messages

        processing_results_df = pd.merge(inst_pos_processing_results_df, cash_pos_processing_results_df, on='msg_id')
        successful_message_ids = processing_results_df[
            (processing_results_df['inst_result'] == True) & (processing_results_df['cash_result'] == True)
        ]['msg_id'].to_list()
        failed_message_ids = processing_results_df[
            (processing_results_df['inst_result'] == False) | (processing_results_df['cash_result'] == False)
        ]['msg_id'].to_list()

        # place requests on queue for ladder processing
        ladder_df = queue_df[queue_df['id'].isin(successful_message_ids)]
        trade_ids = ladder_df['source_id'].to_list()
        trade_df = pd.DataFrame(list(trade.objects.filter(pk__in=trade_ids).values()))
        trade_df = trade_df[['id', 'trade_datetime', 'settlement_date']]
        ladder_df = pd.merge(ladder_df, trade_df, left_on='source_id', right_on='id')

        msg_ids = ladder_df['id_x'].to_list()

        ladder_df['source'] = 'msg_queue'
        ladder_df['source_id'] = ladder_df['id_x']
        ladder_df['destination'] = 'asset_ladder'
        ladder_df['process'] = 'ASSET_MANAGER'
        ladder_df['arg2'] = ladder_df['trade_datetime']
        ladder_df['arg4'] = ladder_df['settlement_date']
        ladder_df['flag'] = 'N'
        ladder_df = ladder_df.drop(columns=['id_x', 'id_y', 'created', 'updated', 'trade_datetime', 'settlement_date'])

        # is placing asset ladder requests fails, mark as failed messages
        if not save_df_to_db(ladder_df, 'msg_queue'):
            failed_message_ids.append(msg_ids)
        else:
            ladder_df['destination'] = 'cash_ladder'
            ladder_df['process'] = 'CASH_MANAGER'

            # is placing cash ladder requests fails, mark as failed messages
            if not save_df_to_db(ladder_df, 'msg_queue'):
                failed_message_ids.append(msg_ids)

            else:
                # flag sucesfully processed messages
                set_processing_flag(successful_message_ids, 'X')

        # flag failed messages
        set_processing_flag(failed_message_ids, 'Z')

    def process_new_trades(self):
        queue_df = select_proc_flag_from_queue('FLOW_BOOKER', 'N')
        trade_df = queue_df[queue_df['source'] == 'accounting_trade']

        # place a request on queue for position manager to check
        # if these are new positions
        msg_ids = trade_df['id'].tolist()

        trade_df['arg1'] = trade_df['source_id']
        trade_df['source_id'] = trade_df['id']
        trade_df['source'] = 'msg_queue'
        trade_df['destination'] = 'accounting_instrument_position'
        trade_df['process'] = 'POS_MANAGER'
        trade_df = trade_df.drop(columns=['id', 'created', 'updated'])

        # if placing request fails, process again on the next run
        if save_df_to_db(trade_df, 'msg_queue'):
            set_processing_flag(msg_ids, 'P')
