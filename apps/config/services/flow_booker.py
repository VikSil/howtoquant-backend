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
from apps.accounting.models import trade, asset_flow, instrument_position
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

    def process_instrument_flow(self, source_id, position_id):

        try:
            # filter for an existing object via the Generic Key
            trade_line = trade.objects.get(pk=source_id)
            inst_position = instrument_position.objects.filter(pk=position_id).first()
            flow_line = asset_flow.objects.filter(
                position_id=position_id, source=ContentType.objects.get_for_model(inst_position).id
            )
            if not flow_line:
                # new trade flow
                direction = 1
                if trade_line.bs_indicator == 'S':
                    direction = -1

                new_asset_flow = asset_flow.objects.create(
                    source_fk=inst_position,
                    trade_date=trade_line.trade_datetime,
                    settlement_date=trade_line.settlement_date,
                    quantity=trade_line.quantity * direction,
                    price=trade_line.price * trade_line.trade_settlement_xrate,
                    asset_flow_type=asset_flow_type.objects.get(type_name='Instrument Flow'),
                    ccy=trade_line.settlement_ccy,
                    xrate=trade_line.settlement_base_xrate,
                )
                new_asset_flow.save()

            else:
                # existing flow handling to be implemented with trade amendments
                pass

        except Exception as e:
            logger.debug(f'An error occured while processing instrument flow for trade: {source_id}')
            return False

        return True

    def process_new_positions(self):
        queue_df = select_proc_flag_from_queue('FLOW_BOOKER', 'F')
        inst_flow_df = queue_df.drop(queue_df.columns.difference(['id', 'source_id', 'arg1']), axis=1)

        inst_pos_processing_results = [
            (row[0], self.process_instrument_flow(row[1], row[2]))
            for row in zip(
                inst_flow_df['id'],
                inst_flow_df['source_id'],
                inst_flow_df['arg1'],
            )
        ]

    def process_new_trades(self):
        queue_df = select_proc_flag_from_queue('FLOW_BOOKER', 'N')
        trade_df = queue_df[queue_df['source'] == 'accounting_trade']

        # Place a request on queue for position manager to check
        # if these are new positions
        msg_ids = trade_df['id'].tolist()

        trade_df['arg1'] = trade_df['source_id']
        trade_df['source_id'] = trade_df['id']
        trade_df['source'] = 'msg_queue'
        trade_df['destination'] = 'accounting_instrument_position'
        trade_df['process'] = 'POS_MANAGER'
        trade_df = trade_df.drop(columns=['id'])

        # if placing request fails, process again on the next run
        if save_df_to_db(trade_df, 'msg_queue'):
            set_processing_flag(msg_ids, 'P')
