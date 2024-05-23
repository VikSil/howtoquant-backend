from pandas_datareader import data as web
import yfinance as yfin
from django.utils import timezone
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

from .models import value_field, download, download_tickers, download_data
from apps.classifiers.models import market_data_source
from apps.staticdata.models import organization, identifier

def download_market_data(source_name: str, tickers: list, start_dt, end_dt):

    # pd.set_option('display.float_format', '{:.10f}'.format) # forces 10 dp formatting on print
    new_market_data = pd.DataFrame()
    try:
        new_download = save_download(start_dt, end_dt)
        save_download_tickers(tickers, new_download)
        source = market_data_source.objects.get(source_name=source_name)

        for ticker in tickers:
            download_batch = eval(
                f"{source.function_name}(ticker_in, start_dt_in, end_dt_in)",
                {
                    # REFACTOR THIS TO PASS IN **KWARGS AND THINK ABOUT INJECTION ATTACKS
                    'ticker_in': ticker,
                    'start_dt_in': start_dt,
                    'end_dt_in': end_dt,
                    'get_yf_price_data': get_yf_price_data,
                },
            )

            if download_batch is not None:
                
                ticker_id = identifier.objects.get(code=ticker).id
                instrument_id = identifier.objects.get(code=ticker).instrument.id
                # THE CORRESPONDING TRANSFORMATION FUNCTION SHOULD BE RETRIEVED FROM DB AS WELL
                save_batch = transform_yf_data(download_batch, new_download.id, ticker_id, instrument_id)
                new_market_data = pd.concat([new_market_data, save_batch])

            new_market_data.reset_index()
            save_download_data(new_market_data)

        new_download.complete_datetime = timezone.now()
        new_download.pending = 0
        new_download.save()

        return new_download.id

    except Exception as e:
        # NEED TO HAVE A THINK OF WHAT CAN GO WRONG AND HOW TO HANDLE IT
        print(e)
        pass


def get_yf_price_data(ticker: str, start_dt, end_dt):
    try:
        yfin.pdr_override()
        df = web.get_data_yahoo(ticker, start=start_dt, end=end_dt)

        if not df.empty:
            return df
        else:
            return None
    except:
        # ADD LOGGING FOR EXCEPTIONS AND HANDLE PER TYPE
        return None


def save_download(start_dt, end_dt):
    try:
        new_download = download.objects.create(
            requested_start_date=start_dt,
            requested_end_date=end_dt,
            owner_org=organization.objects.get(pk=1),
        )
        return new_download

    except Exception as e:
        return e


def save_download_tickers(tickers: list, download: object):
    try:
        for ticker in tickers: # REFACTOR TO RETRIEVE ALL TICKER OBJECTS AT ONCE AND SAVE DATAFRAME IN ONE GO
            add_ticker = download_tickers.objects.create(
                download=download, ticker=identifier.objects.get(code=ticker)
            )

    except Exception as e:
        return e


def save_download_data(data: object):

    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_name = settings.DATABASES['default']['NAME']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']

    try:
        database_url = f'mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = create_engine(database_url, echo=False)
        data.to_sql(download_data._meta.db_table, if_exists='append', con=engine, index=False)

    except Exception as e:
        print(e)


def transform_yf_data(yf_data: object, download_id: int, ticker_id: int, instrument_id: int):
    transformed_data = pd.DataFrame()
    for series_name, series in yf_data.items():
        value_field_id = value_field.objects.get(field_name=series_name).id

        d = {
            'bid_price': series,
            'ask_price': series,
            'download_id': download_id,
            'instrument_id': instrument_id,
            'ticker_id': ticker_id,
            'value_field_id': value_field_id,
        }
        series_data = pd.DataFrame(d)
        series_data['value_date'] = series_data.index

        transformed_data = pd.concat([transformed_data, series_data])

    return transformed_data
