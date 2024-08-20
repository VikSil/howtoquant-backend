# global imports
import inspect
import logging
import os
import pandas as pd
import sys
from django_cron import CronJobBase, Schedule

# local imports

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  # add parent dir to path to import upstream modules

from ..models import msg_queue
from .utils_queue import select_proc_flag_from_queue, set_processing_flag, set_arguements
from apps.accounting.models import trade, instrument_position, cash_position

logger = logging.getLogger(__name__)


class PositionManager(CronJobBase):

    FREQUENCY_IN_MINS = 1

    schedule = Schedule(run_every_mins=FREQUENCY_IN_MINS)
    code = 'config.position_manager'

    def do(self):

        queue_df = select_proc_flag_from_queue('POS_MANAGER', 'N')
        positions_df = queue_df[queue_df['destination'] == 'accounting_instrument_position']

        # extract trades from DB
        trade_ids = positions_df['arg1'].tolist()
        trade_df = pd.DataFrame(list(trade.objects.filter(pk__in=trade_ids).values()))

        # reduce to one line per instrument-book-strategy-account-trade_ccy-settle_ccy combo
        trade_df = self.reduce_trade_df(trade_df)

        # check for each line if exists in instrument_position table - if not, then create
        inst_position_results = [
            (row[0], *self.create_instrument_positions(row[1], row[2], row[3], row[4]))
            for row in zip(
                trade_df['id'],
                trade_df['instrument_id'],
                trade_df['book_id'],
                trade_df['strategy_id'],
                trade_df['account_id'],
            )
        ]

        inst_position_df = pd.DataFrame(inst_position_results, columns=['id', 'position_id', 'position_error'])
        trade_df = pd.merge(trade_df, inst_position_df, on='id')

        # check for each line if exists in cash_position table - if not, then create
        trade_ccy_results = [
            (row[0], *self.create_cash_positions(row[1], row[2], row[3], row[4], row[5]))
            for row in zip(
                trade_df['id'],
                trade_df['ccy_id'],
                trade_df['book_id'],
                trade_df['strategy_id'],
                trade_df['account_id'],
                trade_df['position_id'],
            )
        ]

        settlement_ccy_results = [
            (row[0], *self.create_cash_positions(row[1], row[2], row[3], row[4], row[5]))
            for row in zip(
                trade_df['id'],
                trade_df['settlement_ccy_id'],
                trade_df['book_id'],
                trade_df['strategy_id'],
                trade_df['account_id'],
                trade_df['position_id'],
            )
        ]

        trade_ccy_position_df = pd.DataFrame(
            trade_ccy_results, columns=['id', 'trade_ccy_position_id', 'trade_ccy_position_error']
        )
        settlement_ccy_position_df = pd.DataFrame(
            settlement_ccy_results, columns=['id', 'settlement_ccy_position_id', 'settlement_ccy_position_error']
        )
        trade_df = pd.merge(trade_df, trade_ccy_position_df, on='id')
        trade_df = pd.merge(trade_df, settlement_ccy_position_df, on='id')

        positions_df['arg1'] = positions_df['arg1'].astype(int)
        positions_df = pd.merge(positions_df, trade_df, left_on='arg1', right_on='id')

        successful_positions_df = positions_df[
            (positions_df['position_error'] == False)
            & (positions_df['trade_ccy_position_error'] == False)
            & (positions_df['settlement_ccy_position_error'] == False)
        ]

        failed_positions_df = positions_df[
            (positions_df['position_error'] == True)
            | (positions_df['trade_ccy_position_error'] == True)
            | (positions_df['settlement_ccy_position_error'] == True)
        ]

        # flag processed messages
        set_processing_flag(list(successful_positions_df['id_x']), 'X')
        set_processing_flag(list(failed_positions_df['id_x']), 'Z')

        # communicate back to the originating messages
        set_argument_results = [
            set_arguements(id=row[0], arg1=row[1], arg2=row[2], arg3=row[3])
            for row in zip(
                successful_positions_df['source_id'],
                successful_positions_df['position_id'],
                successful_positions_df['trade_ccy_position_id'],
                successful_positions_df['settlement_ccy_position_id'],
            )
        ]

        if False in set_argument_results:
            logger.debug(
                f'An error occured while sending one of these messages back to FlowBroker: {successful_positions_df}'
            )
        else:
            set_processing_flag(list(successful_positions_df['source_id']), 'F')

        set_processing_flag(list(failed_positions_df['source_id']), 'Y')

    def reduce_trade_df(self, data):
        try:
            data = data.drop(
                data.columns.difference(
                    [
                        'id',
                        'instrument_id',
                        'book_id',
                        'strategy_id',
                        'account_id',
                        'ccy_id',
                        'settlement_ccy_id',
                    ]
                ),
                axis=1,
            )
            data = data.drop_duplicates()

        except Exception as e:
            logger.debug(f'Exception occured while reducing trade dataframe: {e}')

        return data

    def create_instrument_positions(self, instrument, book, strategy, account):
        try:
            position = instrument_position.objects.filter(
                instrument_id=instrument,
                book_id=book,
                strategy_id=strategy,
                account_id=account,
            ).first()
            if not position:
                position = instrument_position.objects.create(
                    instrument_id=instrument,
                    book_id=book,
                    strategy_id=strategy,
                    account_id=account,
                )
                position.save()

            return position.id, False

        except Exception as e:
            logger.debug(f'Exception occured while checking for instrument position: {e}')
            logger.debug(f'Input data: {instrument}, {book}, {strategy}, {account}')
            return None, True

    def create_cash_positions(self, ccy, book, strategy, account, inst_position):
        try:
            position = cash_position.objects.filter(
                ccy_id=ccy,
                book_id=book,
                strategy_id=strategy,
                account_id=account,
                instrument_position_id=inst_position,
            ).first()
            if not position:
                position = cash_position.objects.create(
                    ccy_id=ccy,
                    book_id=book,
                    strategy_id=strategy,
                    account_id=account,
                    instrument_position_id=inst_position,
                )
                position.save()

            return position.id, False

        except Exception as e:
            logger.debug(f'Exception occured while checking for currency position: {e}')
            logger.debug(f'Input data: {ccy}, {book}, {strategy}, {account}, {inst_position}')
            return None, True
