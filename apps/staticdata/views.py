from django.shortcuts import render
from django.db import connection

from .models import identifier_type
from .queries import *

from howtoquant.utils import *

# Create your views here.


def index(request):
    """
    Function for the main landing page
    """

    return render(
        request,
        "index.html",
    )


def raw_sql_example(request):

    data = identifier_type.objects.raw(identifier_type_select_all)
    # data = identifier_type.objects.raw(identifier_type_queries['select_all'])[:2]# slicing = return first two rows

    # iterrating over the returned rows
    for item in identifier_type.objects.raw(identifier_type_select_all):
        print(str(item.id) + " " + item.type_name)

    # mapping
    identifier_types_map = {'id': 'id', 'identifier_type': 'type_name'}
    objs = identifier_type.objects.raw(identifier_type_select_all, translations=identifier_types_map)
    ident_type = objs[1].type_name
    print(ident_type)

    print(data)

    return render(request, "sandbox.html", {'data': data})


def direct_sql_example(request):



    cursor = connection.cursor()
    cursor.execute(identifier_type_select_where_id, [1])
    data = dictfetch(cursor, 2) # alternatively -  dictfetchone | dictfetchall
    print(data)

    return render(request, "sandbox.html", {'data': data})
