from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import identifier_type
from .queries import *
from .serializers import *

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
    data = dictfetch(cursor, 2)  # alternatively -  dictfetchone | dictfetchall
    print(data)

    return render(request, "sandbox.html", {'data': data})


@api_view(['GET', 'POST'])
def api_identifier_types(request):

    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute(identifier_type_select_all)
        data = dictfetchall(cursor)
        serializer = identifier_type_serializer(data, many=True)
        print("this is serializer.data")
        print(serializer.data)
        return JsonResponse({"identifier_types": serializer.data}, safe=False)

    elif request.method == 'POST':
        serializer = identifier_type_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def api_identifier_type(request, id):
    try:
        data = identifier_type.objects.get(pk=id)
    except identifier_type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = identifier_type_serializer(data)
        return Response({"identifier_type": serializer.data})

    elif request.method == 'PUT':        
        serializer = identifier_type_serializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        data.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        
