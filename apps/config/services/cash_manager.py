# global imports
import logging
import pandas as pd

from django.core.exceptions import ObjectDoesNotExist
from django_cron import CronJobBase, Schedule

# local imports
from .utils_queue import select_proc_flag_from_queue, set_processing_flag
from .utils_services import (
    aggregate_flows_df,
    expand_flows_df,
    mark_ladder_processing_msgs,
    reduce_ladder_df,
    update_ladder,
)
from apps.accounting.models import asset_flow, cash_ladder
from apps.classifiers.models import asset_flow_type
from howtoquant.utils import save_df_to_db

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
        cash_ladder_df = reduce_ladder_df(cash_ladder_df, 'arg3', 'arg4')
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
        mark_ladder_processing_msgs(processing_results)

    def process_line(self, cash_pos_id, date):
        try:
            # find the flows data
            source_id = asset_flow_type.objects.get(type_name='Cash Flow')
            flows_df = pd.DataFrame(
                list(
                    asset_flow.objects.filter(
                        asset_flow_type=source_id, position_id=cash_pos_id, settlement_date__gte=date
                    ).values()
                )
            )
            position_id = flows_df['position_id'][0]
            flows_df = aggregate_flows_df(flows_df, is_cash_ladder=True)

            # get the earliest date from ladder
            try:
                first_ladder_day = cash_ladder.objects.filter(position_id=position_id).earliest('date').date.date()
            except ObjectDoesNotExist:  # no records in cash ladder for this position
                flows_df = expand_flows_df(flows_df, position_id)
                return save_df_to_db(flows_df, 'cash_ladder')

            else:  # records in cash_ladder already exist
                return update_ladder(flows_df, position_id, first_ladder_day, is_cash_ladder=True)

        except Exception as e:
            logger.debug(f'Exception occured while extracting flow data: {e}')
            return False
