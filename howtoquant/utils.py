def dictfetch(cursor, rowcount):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchmany(rowcount)]

def dictfetchone(cursor, rowcount):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchone()]

def dictfetchall(cursor, rowcount):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
