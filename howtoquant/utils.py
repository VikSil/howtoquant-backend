from django.db import connection

def dict_fetch(query, rowcount, *args):
    cursor = connection.cursor()
    cursor.execute(query, *args)
    desc = cursor.description
    rows = cursor.fetchmany(rowcount)
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
        return [dict(zip([col[0] for col in desc], row))]
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

def delete_where(query, *args):
    cursor = connection.cursor()
    cursor.execute(query, *args)
    connection.commit()
    return cursor.rowcount 
        