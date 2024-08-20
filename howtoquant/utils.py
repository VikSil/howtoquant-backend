import logging
from django.conf import settings
from django.db import connection
from sqlalchemy import create_engine


from apps.config.models import msg_queue
from apps.accounting.models import asset_flow

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

    try:
        database_url = f'mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = create_engine(database_url, echo=False)
        data.to_sql(table, if_exists='append', con=engine, index=False)

    except Exception as e:
        logger.debug(f'Exception occured while saving data to queue: {e}')
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
