# global imports
import inspect
import logging
import os
import pandas as pd
import sys

from django.conf import settings
from sqlalchemy import create_engine

# local imports

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)  # add parent dir to path to import upstream modules

from ..models import msg_queue

logger = logging.getLogger(__name__)


def queue_to_pandas():
    df = pd.DataFrame(list(msg_queue.objects.all().values()))
    return df


def save_df_to_queue(data: object):
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_name = settings.DATABASES['default']['NAME']
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']

    try:
        database_url = f'mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = create_engine(database_url, echo=False)
        data.to_sql(msg_queue._meta.db_table, if_exists='append', con=engine, index=False)

    except Exception as e:
        logger.debug(f'Exception occured while saving data to queue: {e}')


def select_flag_from_queue(flag: str):
    queue_df = queue_to_pandas()
    df = queue_df[queue_df.flag.str.contains(flag)]
    return df


def select_proc_flag_from_queue(process: str, flag: str):
    queue_df = queue_to_pandas()
    df = queue_df[queue_df.flag.str.contains(flag) & queue_df.process.str.contains(process)]
    return df


def set_arguements(id, **kwargs):
    try:
        if 'arg1' in kwargs:
            msg_queue.objects.filter(pk=id).update(arg1=kwargs['arg1'])
        if 'arg2' in kwargs:
            msg_queue.objects.filter(pk=id).update(arg2=kwargs['arg2'])
        if 'arg3' in kwargs:
            msg_queue.objects.filter(pk=id).update(arg3=kwargs['arg3'])
        if 'arg4' in kwargs:
            msg_queue.objects.filter(pk=id).update(arg4=kwargs['arg4'])
        return True

    except Exception as e:
        logger.debug(f'Exception occured while setting arguments to the queue: {e}')
        return False


def set_processing_flag(ids, proc_flag):
    msg_queue.objects.filter(pk__in=ids).update(flag=proc_flag)
