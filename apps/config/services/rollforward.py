# global imports
import logging
import pandas as pd

from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule

# local imports
from .utils_queue import select_proc_flag_from_queue, set_processing_flag
from apps.accounting.models import asset_ladder, cash_ladder
from apps.config.utils import add_to_msg_queue
from howtoquant.utils import save_df_to_db

logger = logging.getLogger(__name__)


class Rollforward(CronJobBase):

    FREQUENCY_IN_MINS = 15

    schedule = Schedule(run_every_mins=FREQUENCY_IN_MINS)
    code = 'config.rollforward'

    def do(self):
        if self.check_if_new_day():
            self.run_rollforward()

    def check_if_new_day(self):
        today = datetime.today().date().strftime('%Y-%m-%d')
        queue_df = select_proc_flag_from_queue('ROLLFORWARD', 'X')
        if today not in queue_df['arg1'].values:
            return True
        return False

    def run_rollforward(self):
        try:
            today = datetime.today().date()
            queue_df = select_proc_flag_from_queue('ROLLFORWARD', 'N')
            cash_manager_df = select_proc_flag_from_queue('CASH_MANAGER', 'N')
            asset_manager_df = select_proc_flag_from_queue('ASSET_MANAGER', 'N')

            # if no ladder processing happening
            if queue_df.empty and cash_manager_df.empty and asset_manager_df.empty:
                # signal to other services that rollforward will run
                add_to_msg_queue('cron_job', '0', 'ladders', 'ROLLFORWARD', arg1=today)

            # if already signaled intent to run - proceed
            elif not queue_df.empty:
                yesterday = (datetime.today() - timedelta(days=1)).date()

                yesterday_cash_ladder_df = pd.DataFrame(list(cash_ladder.objects.filter(date__gte=yesterday).values()))
                try:
                    yesterday_cash_ladder_df = yesterday_cash_ladder_df.groupby('position_id').filter(
                        lambda x: len(x) == 1
                    )
                except KeyError:  # empty dataframe cannot be grouped
                    result1 = True
                else:
                    yesterday_cash_ladder_df = yesterday_cash_ladder_df[
                        pd.to_datetime(yesterday_cash_ladder_df['date']).dt.date < today
                    ]

                    today_cash_ladder_df = yesterday_cash_ladder_df.drop(
                        columns=['id', 'date', 'created', 'updated'], axis=1
                    )
                    today_cash_ladder_df['date'] = today
                    result1 = save_df_to_db(today_cash_ladder_df, 'cash_ladder')

                yesterday_asset_ladder_df = pd.DataFrame(
                    list(asset_ladder.objects.filter(date__date__gte=yesterday).values())
                )

                try:
                    today_asset_ladder_df = yesterday_asset_ladder_df.drop(
                        columns=['id', 'date', 'created', 'updated'], axis=1
                    )
                except KeyError:  # empty dataframe cannot be grouped
                    result2 = True
                else:

                    today_asset_ladder_df['date'] = today
                    result2 = save_df_to_db(today_asset_ladder_df, 'asset_ladder')

                if result1 and result2:
                    set_processing_flag(queue_df['id'].to_list(), 'X')

        except Exception as e:
            logger.debug(f'Exception occured during rollforward: {e}')
