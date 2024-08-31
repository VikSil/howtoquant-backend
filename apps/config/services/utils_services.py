import logging
import pandas as pd

from datetime import datetime, timedelta

from .utils_queue import set_processing_flag
from apps.accounting.models import asset_ladder, cash_ladder
from howtoquant.utils import save_df_to_db, update_df_to_db

logger = logging.getLogger(__name__)

pd.options.mode.chained_assignment = None


def add_dummy_valuation(flows_df):
    '''
    Function adds temporary market value and price of zero
    and value scheme of one for all lines in asset ladder

    To be replaced by PricingManager service
    '''

    flows_df['market_value'] = 0
    flows_df['market_price'] = 0
    flows_df['value_scheme_id'] = 1

    return flows_df


def aggregate_flows_df(flows_df, is_cash_ladder):
    if is_cash_ladder:
        date_column_name = 'settlement_date'
    else:
        date_column_name = 'trade_date'

    # aggregate qty for each date
    flows_df = flows_df.drop(flows_df.columns.difference([date_column_name, 'quantity']), axis=1)
    flows_df.rename(columns={date_column_name: 'date'}, inplace=True)
    flows_df['date'] = pd.to_datetime(flows_df['date']).dt.date
    flows_df = flows_df.groupby('date')['quantity'].sum().reset_index()

    return flows_df


def expand_flows_df(flows_df, position_id):
    flows_df = find_cumulative_flows(flows_df)

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


def find_cumulative_flows(flows_df):
    # adds quantity on each previous date to to quantity the next date
    flows_df = flows_df.sort_values(by='date').reset_index(drop=True)
    flows_df['previous_quantity'] = flows_df['quantity'].shift(1, fill_value=0)
    flows_df['cumulative_quantity'] = flows_df['previous_quantity'].cumsum() + flows_df['quantity']
    flows_df = flows_df.drop(columns=['quantity', 'previous_quantity'])
    flows_df = flows_df.rename(columns={'cumulative_quantity': 'quantity'})

    return flows_df


def mark_ladder_processing_msgs(processing_results):
    try:
        processing_results_df = pd.DataFrame(processing_results, columns=['msg_id', 'result'])
        successful_message_ids = processing_results_df.loc[processing_results_df['result'] == True, 'msg_id'].tolist()
        failed_message_ids = processing_results_df.loc[processing_results_df['result'] == False, 'msg_id'].tolist()
        set_processing_flag(successful_message_ids, 'X')
        set_processing_flag(failed_message_ids, 'Z')

    except Exception as e:
        logger.debug(f'Exception occured while setting flags on ladder processing messages: {e}')


def reduce_ladder_df(ladder_df, trans_column, date_column):
    ladder_df = ladder_df.drop(ladder_df.columns.difference(['id', trans_column, date_column]), axis=1)
    ladder_df[date_column] = pd.to_datetime(ladder_df[date_column], format='mixed').dt.date
    ladder_df = ladder_df.sort_values([trans_column, date_column])
    ladder_df = ladder_df.drop_duplicates(subset=trans_column, keep='first')

    return ladder_df


def update_ladder(flows_df, position_id, first_ladder_day, is_cash_ladder):
    if is_cash_ladder:
        last_ladder_day = cash_ladder.objects.filter(position_id=position_id).latest('date').date
        ladder_name_short = 'cash_ladder'
        ladder_name_long = 'accounting_cash_ladder'
    else:
        last_ladder_day = asset_ladder.objects.filter(position_id=position_id).latest('date').date
        ladder_name_short = 'asset_ladder'
        ladder_name_long = 'accounting_asset_ladder'

    latest_flow_date = flows_df['date'].iloc[-1]
    earliest_flow_date = flows_df['date'][0]

    # if earliest new flow earlier than cash_ladder records - entire ladder will be recalculated
    if earliest_flow_date < first_ladder_day:
        flows_df = expand_flows_df(flows_df, position_id)
        if not is_cash_ladder:
            flows_df = add_dummy_valuation(flows_df)

        # rows that don't exist in ladder will be inserted
        flows_before_df = flows_df[pd.to_datetime(flows_df['date']).dt.date < first_ladder_day]

        # rows that already exist in ladder will be updated
        flows_overlap_df = flows_df[
            (pd.to_datetime(flows_df['date']).dt.date >= first_ladder_day)
            & (pd.to_datetime(flows_df['date']).dt.date <= last_ladder_day)
        ]
        flows_overlap_df['date'] = flows_overlap_df['date'].dt.strftime('%Y-%m-%d')

        result = save_df_to_db(flows_before_df, ladder_name_short) and update_df_to_db(
            flows_overlap_df, ladder_name_long, ['date', 'position_id']
        )

    else:
        # if earliest new flow overlaps with cash_ladder records
        if earliest_flow_date <= last_ladder_day:
            day_before = earliest_flow_date - timedelta(days=1)
            if is_cash_ladder:
                previous_record = cash_ladder.objects.filter(date=day_before).first()
            else:
                previous_record = asset_ladder.objects.filter(date=day_before).first()
            if previous_record is not None:
                qty_day_before = previous_record.quantity
            else:
                qty_day_before = 0

            flows_df = expand_flows_df(flows_df, position_id)
            if not is_cash_ladder:
                flows_df = add_dummy_valuation(flows_df)

            # update df with the previous day qty from ladder
            flows_df['quantity'] = flows_df['quantity'] + qty_day_before
            flows_overlap_df = flows_df[pd.to_datetime(flows_df['date']).dt.date <= last_ladder_day]
            flows_overlap_df['date'] = flows_overlap_df['date'].dt.strftime('%Y-%m-%d')
            result = update_df_to_db(flows_overlap_df, ladder_name_long, ['date', 'position_id'])

        # earliest new flow after cash_ladder records
        else:
            if is_cash_ladder:

                qty_last_ladder_day = cash_ladder.objects.get(date=last_ladder_day).quantity
            else:
                qty_last_ladder_day = asset_ladder.objects.get(date=last_ladder_day).quantity

            last_ladder_day_df = pd.DataFrame({'date': [last_ladder_day], 'quantity': [qty_last_ladder_day]})
            flows_df = pd.concat([flows_df, last_ladder_day_df], ignore_index=True)
            flows_df = expand_flows_df(flows_df, position_id)
            if not is_cash_ladder:
                flows_df = add_dummy_valuation(flows_df)

            result = True

    # if projected cashflow dates exceed cash ladder dates
    if is_cash_ladder and last_ladder_day < latest_flow_date:
        flows_future_df = flows_df[pd.to_datetime(flows_df['date']).dt.date > last_ladder_day]
        result = result and save_df_to_db(flows_future_df, ladder_name_short)

    return result
