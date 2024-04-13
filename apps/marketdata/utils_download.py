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

    market_data = pd.DataFrame() 
    try:
        request_value_spec = value_spec.objects.filter(pk=spec_id)[0]
        new_download = save_download(request_value_spec, start_dt, end_dt)

        save_download_tickers(tickers, new_download)

        source = fetch_one_value(value_spec_select_name_by_id, [1])
        if source == 'YF Download':

            for ticker in tickers:
                download_batch = get_yahoo_data(ticker, start_dt, end_dt)

                if download_batch is not None:
                    for series_name, series in download_batch.items():

                        request_ticker = identifier.objects.filter(code=ticker)[0]
                        request_instrument = request_ticker.instrument
                        data_value_field = value_field.objects.filter(field_name=series_name)[0]
                        # DOING THIS IN A LOOP IS INCREADIBLY SLOW
                        # NEED TO REWRITE BY SENDING ALL market_data TO THE DB once
                        if data_value_field:
                            save_download_data(
                                new_download.id,
                                data_value_field.id,
                                spec_id,
                                request_ticker.id,
                                request_instrument.id,
                                bid_price=series,
                                ask_price=series,
                            )

                    # market_data = pd.concat([market_data, download_batch])

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


def save_download_data(
    download_id, value_field_id, value_spec_id, ticker_id, instrument_id, **kwargs
):
    save_df = pd.DataFrame(kwargs)
    save_df['download_id'] = download_id
    save_df['value_date'] = save_df.index
    save_df['instrument_id'] = instrument_id
    save_df['value_field_id'] = value_field_id
    save_df['value_spec_id'] = value_spec_id
    save_df['ticker_id'] = ticker_id

    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_name = settings.DATABASES['default']['NAME']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']

    try:
        database_url = f'mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        print(database_url)
        engine = create_engine(database_url, echo = False)
        save_df.to_sql(download_data._meta.db_table, if_exists = 'append', con = engine, index = False)

    except Exception as e:
        print(e)
