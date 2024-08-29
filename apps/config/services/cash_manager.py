# global imports
import inspect
import logging
import pandas as pd
import os
import sys

from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django_cron import CronJobBase, Schedule

# local imports

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  # add parent dir to path to import upstream modules

from .utils_queue import select_proc_flag_from_queue, set_processing_flag
from apps.accounting.models import asset_flow, cash_ladder
from apps.classifiers.models import asset_flow_type
from howtoquant.utils import save_df_to_db, update_df_to_db

logger = logging.getLogger(__name__)


class CashManager(CronJobBase):

    FREQUENCY_IN_MINS = 1

    schedule = Schedule(run_every_mins=FREQUENCY_IN_MINS)
    code = 'config.cash_manager'

    def do(self):
        queue_df = select_proc_flag_from_queue('CASH_MANAGER', 'N')
        cash_ladder_df = queue_df[queue_df['destination'] == 'cash_ladder']

        # reduce the msg queue - for each position_id pick the line with the oldest arg4
        msg_queue_ids = cash_ladder_df['id'].to_list()
        cash_ladder_df = self.reduce_ladder_df(cash_ladder_df)
        msg_queue_ids_short = cash_ladder_df['id'].to_list()

        # mark newer msg queue lines as processed
        msg_queue_ids_diff = list(set(msg_queue_ids) - set(msg_queue_ids_short))
        set_processing_flag(msg_queue_ids_diff, 'X')

        processing_results = [
            (row[0], self.process_line(row[1], row[2]))
            for row in zip(
                cash_ladder_df['id'],
                cash_ladder_df['arg3'],
                cash_ladder_df['arg4'],
            )
        ]
        # mark processed lines as done or failed
        processing_results_df = pd.DataFrame(processing_results, columns=['msg_id', 'result'])
        successful_message_ids = processing_results_df.loc[processing_results_df['result'] == True, 'msg_id'].tolist()
        failed_message_ids = processing_results_df.loc[processing_results_df['result'] == False, 'msg_id'].tolist()
        set_processing_flag(successful_message_ids, 'X')
        set_processing_flag(failed_message_ids, 'Z')

    def expand_flows_df(self, flows_df, position_id):
        flows_df = self.find_cumulative_flows(flows_df)

        # forward fill missing dates in flows_df
        flows_df.set_index('date', inplace=True)
        earliest_flow_date = flows_df.index.min()
        date_range = pd.date_range(start=earliest_flow_date, end=max(datetime.today().date(), flows_df.index.max()))
        flows_df = flows_df.reindex(date_range)
        flows_df['quantity'] = flows_df['quantity'].ffill()
        flows_df.reset_index(inplace=True)
        flows_df.rename(columns={'index': 'date'}, inplace=True)
        flows_df['position_id'] = position_id

        return flows_df

    def find_cumulative_flows(self, flows_df):
        # adds quantity on each previous date to to quantity the next date
        flows_df = flows_df.sort_values(by='date').reset_index(drop=True)
        flows_df['previous_quantity'] = flows_df['quantity'].shift(1, fill_value=0)
        flows_df['cumulative_quantity'] = flows_df['previous_quantity'].cumsum() + flows_df['quantity']
        flows_df = flows_df.drop(columns=['quantity', 'previous_quantity'])
        flows_df = flows_df.rename(columns={'cumulative_quantity': 'quantity'})

        return flows_df

    def process_line(self, cash_pos_id, date):
        try:
            # for each position_id find all asset_flow records with source_id = 2 and
            # settlement date equal or newer than queue arg4
            source_id = asset_flow_type.objects.get(type_name='Cash Flow')
            flows_df = pd.DataFrame(
                list(
                    asset_flow.objects.filter(
                        asset_flow_type=source_id, position_id=cash_pos_id, settlement_date__gte=date
                    ).values()
                )
            )
            position_id = flows_df['position_id'][0]

            # aggregate qty for each date
            flows_df = flows_df.drop(flows_df.columns.difference(['settlement_date', 'quantity']), axis=1)
            flows_df.rename(columns={'settlement_date': 'date'}, inplace=True)
            flows_df['date'] = pd.to_datetime(flows_df['date']).dt.date
            flows_df = flows_df.groupby('date')['quantity'].sum().reset_index()

            # get the earliest date from ladder
            try:
                first_ladder_day = cash_ladder.objects.filter(position_id=position_id).earliest('date').date.date()
            except ObjectDoesNotExist:  # no records in cash ladder for this position
                flows_df = self.expand_flows_df(flows_df, position_id)
                return save_df_to_db(flows_df, 'cash_ladder')

            else:  # records in cash_ladder already exist
                last_ladder_day = cash_ladder.objects.filter(position_id=position_id).latest('date').date.date()
                latest_flow_date = flows_df['date'].iloc[-1]
                earliest_flow_date = flows_df['date'][0]

                # if earliest new flow earlier than cash_ladder records - entire ladder will be recalculated
                if earliest_flow_date < first_ladder_day:
                    flows_df = self.expand_flows_df(flows_df, position_id)

                    # rows that don't exist in ladder will be inserted
                    flows_before_df = flows_df[pd.to_datetime(flows_df['date']).dt.date < first_ladder_day]

                    # rows that already exist in ladder will be updated
                    flows_overlap_df = flows_df[
                        (pd.to_datetime(flows_df['date']).dt.date >= first_ladder_day)
                        & (pd.to_datetime(flows_df['date']).dt.date <= last_ladder_day)
                    ]

                    result = save_df_to_db(flows_before_df, 'cash_ladder') and update_df_to_db(
                        flows_overlap_df, 'accounting_cash_ladder', ['date', 'position_id']
                    )

                else:
                    # if earliest new flow overlaps with cash_ladder records
                    if earliest_flow_date <= last_ladder_day:
                        day_before = earliest_flow_date - timedelta(days=1)
                        cash_qty_day_before = cash_ladder.objects.filter(date=day_before).first().quantity
                        flows_df = self.expand_flows_df(flows_df, position_id)

                        # update df with the previous day qty from ladder
                        flows_df['quantity'] = flows_df['quantity'] + cash_qty_day_before
                        flows_overlap_df = flows_df[pd.to_datetime(flows_df['date']).dt.date <= last_ladder_day]
                        result = update_df_to_db(flows_overlap_df, 'accounting_cash_ladder', ['date', 'position_id'])

                    # earliest new flow after cash_ladder records
                    else:
                        cash_qty_last_ladder_day = cash_ladder.objects.get(date=last_ladder_day).quantity
                        last_ladder_day_df = pd.DataFrame(
                            {'date': [last_ladder_day], 'quantity': [cash_qty_last_ladder_day]}
                        )
                        flows_df = pd.concat([flows_df, last_ladder_day_df], ignore_index=True)
                        flows_df = self.expand_flows_df(flows_df, position_id)
                        result = True

                # if flow dates exceed ladder dates
                if last_ladder_day < latest_flow_date:
                    flows_future_df = flows_df[pd.to_datetime(flows_df['date']).dt.date > last_ladder_day]
                    result = result and save_df_to_db(flows_future_df, 'cash_ladder')

                return result

        except Exception as e:
            logger.debug(f'Exception occured while extracting flow data: {e}')
            return False

    def reduce_ladder_df(self, ladder_df):
        ladder_df = ladder_df.drop(ladder_df.columns.difference(['id', 'arg3', 'arg4']), axis=1)
        ladder_df['arg4'] = pd.to_datetime(ladder_df['arg4'], format='mixed').dt.date
        ladder_df = ladder_df.sort_values(['arg3', 'arg4'])
        ladder_df = ladder_df.drop_duplicates(subset='arg3', keep='first')

        return ladder_df
