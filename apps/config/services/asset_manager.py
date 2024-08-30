# global imports
import logging
import pandas as pd

from django.core.exceptions import ObjectDoesNotExist
from django_cron import CronJobBase, Schedule

# local imports
from .utils_queue import select_proc_flag_from_queue, set_processing_flag
from .utils_services import (
    add_dummy_valuation,
    aggregate_flows_df,
    expand_flows_df,
    mark_ladder_processing_msgs,
    reduce_ladder_df,
    update_ladder,
)
from apps.accounting.models import asset_flow, asset_ladder
from apps.classifiers.models import asset_flow_type
from howtoquant.utils import save_df_to_db


logger = logging.getLogger(__name__)


class AssetManager(CronJobBase):

    FREQUENCY_IN_MINS = 1

    schedule = Schedule(run_every_mins=FREQUENCY_IN_MINS)
    code = 'config.asset_manager'

    def do(self):
        rollforward_msg = select_proc_flag_from_queue('ROLLFORWARD', 'N')

        if rollforward_msg.empty:  # only process ladder if Rollforward not in progress
            queue_df = select_proc_flag_from_queue('ASSET_MANAGER', 'N')
            asset_ladder_df = queue_df[queue_df['destination'] == 'asset_ladder']

            # reduce the msg queue - for each position_id pick the line with the oldest arg2
            msg_queue_ids = asset_ladder_df['id'].to_list()
            asset_ladder_df = reduce_ladder_df(asset_ladder_df, 'arg1', 'arg2')
            msg_queue_ids_short = asset_ladder_df['id'].to_list()

            # mark newer msg queue lines as processed
            msg_queue_ids_diff = list(set(msg_queue_ids) - set(msg_queue_ids_short))
            set_processing_flag(msg_queue_ids_diff, 'X')

            processing_results = [
                (row[0], self.process_line(row[1], row[2]))
                for row in zip(
                    asset_ladder_df['id'],
                    asset_ladder_df['arg1'],
                    asset_ladder_df['arg2'],
                )
            ]

            # mark processed lines as done or failed
            mark_ladder_processing_msgs(processing_results)

    def process_line(self, inst_pos_id, date):
        try:
            # find the initial flows data
            source_id = asset_flow_type.objects.get(type_name='Instrument Flow')
            flows_df = pd.DataFrame(
                list(
                    asset_flow.objects.filter(
                        asset_flow_type=source_id, position_id=inst_pos_id, trade_date__gte=date
                    ).values()
                )
            )
            position_id = flows_df['position_id'][0]

            flows_df = aggregate_flows_df(flows_df, is_cash_ladder=False)
            # get the earliest date from ladder
            try:
                first_ladder_day = asset_ladder.objects.filter(position_id=position_id).earliest('date').date.date()
            except ObjectDoesNotExist:  # no records in cash ladder for this position
                flows_df = expand_flows_df(flows_df, position_id)
                flows_df = add_dummy_valuation(flows_df)
                return save_df_to_db(flows_df, 'asset_ladder')

            else:  # records in cash_ladder already exist
                return update_ladder(flows_df, position_id, first_ladder_day, is_cash_ladder=False)

        except Exception as e:
            logger.debug(f'Exception occured while extracting flow data: {e}')
            return False
