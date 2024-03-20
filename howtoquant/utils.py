def dictfetch(cursor, rowcount):
    desc = cursor.description
    rows = cursor.fetchmany(rowcount)
    if rows:
        return [dict(zip([col[0] for col in desc], row)) for row in rows]
    else:
        return None

def dictfetchone(cursor):
    desc = cursor.description
    row = cursor.fetchone()
    if row:
        return [dict(zip([col[0] for col in desc], row))]
    else:
        return None

def dictfetchall(cursor):
    desc = cursor.description
    rows = cursor.fetchall()
    if rows:
        return [dict(zip([col[0] for col in desc], row)) for row in rows]
    else:
        return None
