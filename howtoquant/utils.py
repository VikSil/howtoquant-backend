import logging
from django.conf import settings
from django.db import connection
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from typing import List


from apps.config.models import msg_queue
from apps.accounting.models import asset_flow, cash_ladder

logger = logging.getLogger(__name__)


def dict_fetch(query, rowcount, *args):
    cursor = connection.cursor()
    cursor.execute(query, *args)
    desc = cursor.description
    rows = cursor.fetchmany(rowcount)
    if rows:
        return [dict(zip([col[0] for col in desc], row)) for row in rows]
    else:
        return None


def dict_fetch_all(query, *args):
    cursor = connection.cursor()
    cursor.execute(query, *args)
    desc = cursor.description
    rows = cursor.fetchall()
    if rows:
        return [dict(zip([col[0] for col in desc], row)) for row in rows]
    else:
        return None


def dict_fetch_one(query, *args):
    cursor = connection.cursor()
    cursor.execute(query, *args)
    desc = cursor.description
    row = cursor.fetchone()
    if row:
        return dict(zip([col[0] for col in desc], row))
    else:
        return None


def execute_where(query, *args):
    cursor = connection.cursor()
    cursor.execute(query, list(args))
    connection.commit()
    return cursor.rowcount


def fetch_one_value(query, *args):
    cursor = connection.cursor()
    cursor.execute(query, *args)
    desc = cursor.description
    row = cursor.fetchone()
    if row:
        result = dict(zip([col[0] for col in desc], row))
        return result[desc[0][0]]
    else:
        return None


def list_fetch_all(query, *args):
    cursor = connection.cursor()
    cursor.execute(query, *args)
    rows = cursor.fetchall()
    if rows:
        return sorted([item for row in rows for item in row], key=str.lower)
    else:
        return []


def save_df_to_db(data: object, table_name: str) -> bool:
    '''
    Function takes a dataframe and attempts to save it into the an indicated table
    It is the callers responsibility to make sure that the shape of the data
    matches that of the destination table
    '''
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_name = settings.DATABASES['default']['NAME']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']

    if table_name == 'msg_queue':
        table = msg_queue._meta.db_table
    elif table_name == 'asset_flow':
        table = asset_flow._meta.db_table
    elif table_name == 'cash_ladder':
        table = cash_ladder._meta.db_table

    try:
        database_url = f'mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = create_engine(database_url, echo=False)
        data.to_sql(table, if_exists='append', con=engine, index=False)

    except SQLAlchemyError as e:
        logger.debug(f'Exception occured while inserting data into the database: {e}')
        return False

    return True


def trigger_proc(query, *args):
    cursor = connection.cursor()
    try:
        cursor.callproc(query, *args)
        return 'OK'
    except Exception as e:
        return e
    finally:
        cursor.close()


def update_df_to_db(data: object, table_name: str, matching_columns: List) -> bool:
    '''
    Function takes a dataframe and attempts to update rows in the indicated table
    where values in matching columns is the same as in the dataframe.
    PK column will not be updated, and can be either passed in matching_columns or not
    It is the callers responsibility to make sure that the shape of the data
    matches that of the destination table
    '''
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_name = settings.DATABASES['default']['NAME']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']

    try:
        database_url = f'mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = create_engine(database_url, echo=False)

        with engine.connect() as connection:
            update_queries = [
                text(
                    f""" 
                    UPDATE {table_name} SET
                    {', '.join([f"{col} = :{col}" for col in data.columns if col not in matching_columns])}
                    WHERE  {' AND '.join([f"{col} = :{col}" for col in matching_columns])}
                """
                )
                for row in data.to_dict(orient='records')
            ]

            for query, params in zip(update_queries, data.to_dict(orient='records')):
                connection.execute(query, **params)

    except SQLAlchemyError as e:
        print(e)
        logger.debug(f'Exception occured while updating data in the database: {e}')
        return False

    return True
