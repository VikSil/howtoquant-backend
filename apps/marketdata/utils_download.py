from pandas_datareader import data as web
import yfinance as yfin
from django.utils import timezone
import pandas as pd
from sqlalchemy import create_engine
from django.conf import settings

from .models import value_spec, value_field, download, download_tickers, download_data
from apps.staticdata.models import organization, identifier, instrument
from howtoquant.utils import fetch_one_value
from .db.queries import value_spec_select_name_by_id


def download_spec(spec_id: int, tickers: list, start_dt, end_dt):

    # pd.set_option('display.float_format', '{:.10f}'.format) # forces 10 dp formatting on print
    new_market_data = pd.DataFrame()
    try:
        request_value_spec = value_spec.objects.filter(pk=spec_id)[0]
        new_download = save_download(request_value_spec, start_dt, end_dt)

        save_download_tickers(tickers, new_download)

        source = fetch_one_value(value_spec_select_name_by_id, [1])
        if source == 'YF Download':

            for ticker in tickers:
                download_batch = get_yahoo_data(ticker, start_dt, end_dt)

                if download_batch is not None:

                    ticker_id = identifier.objects.filter(code=ticker)[0].id
                    instrument_id = identifier.objects.filter(code=ticker)[0].instrument.id
                    save_batch = transform_yf_data(download_batch, new_download.id, spec_id, ticker_id, instrument_id)
                    new_market_data = pd.concat([new_market_data, save_batch])

            new_market_data.reset_index()
            save_download_data(new_market_data)

        new_download.complete_datetime = timezone.now()
        new_download.save()

        return new_download.id

    except Exception as e:
        # NEED TO HAVE A THINK OF WHAT CAN GO WRONG AND HOW TO HANDLE IT
        print(e)
        pass


def get_yahoo_data(ticker: str, start_dt, end_dt):
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


def save_download(value_spec: object, start_dt, end_dt):
    try:
        new_download = download.objects.create(
            value_spec=value_spec,
            requested_start_date=start_dt,
            requested_end_date=end_dt,
            owner_org=organization.objects.filter(pk=1)[0],
        )
        new_download.save()
        return new_download

    except Exception as e:
        return e


def save_download_tickers(tickers: list, download: object):
    try:
        for ticker in tickers:
            add_ticker = download_tickers.objects.create(
                download=download, ticker=identifier.objects.filter(code=ticker)[0]
            )
            add_ticker.save()

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


def transform_yf_data(yf_data: object, download_id: int, spec_id: int, ticker_id: int, instrument_id :int):
    transformed_data = pd.DataFrame()
    for series_name, series in yf_data.items():
        value_field_id = value_field.objects.filter(field_name=series_name)[0].id

        d = {
            'bid_price': series,
            'ask_price': series,
            'download_id': download_id,
            'value_spec_id': spec_id,
            'instrument_id': instrument_id,
            'ticker_id': ticker_id,
            'value_field_id': value_field_id,
        }
        series_data = pd.DataFrame(d)
        series_data['value_date'] = series_data.index

        transformed_data = pd.concat([transformed_data, series_data])

    return transformed_data
