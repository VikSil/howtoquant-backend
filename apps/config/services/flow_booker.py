# global imports
import inspect
import os
import pandas as pd
import sys
from django_cron import CronJobBase, Schedule

# local imports

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  # add parent dir to path to import upstream modules

from ..models import msg_queue
from .utils_queue import select_proc_flag_from_queue, set_processing_flag
from howtoquant.utils import save_df_to_db


class FlowBooker(CronJobBase):

    FREQUENCY_IN_MINS = 1

    schedule = Schedule(run_every_mins=FREQUENCY_IN_MINS)
    code = 'config.flow_booker'

    def do(self):
        self.process_new_trades()
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
