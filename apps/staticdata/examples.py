# from django.shortcuts import render
# from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework import generics

# from ..classifiers.models import identifier_type
# from .db.queries import *
# from .serializers import *

# from howtoquant.utils import *


# def raw_sql_example(request):

#     data = identifier_type.objects.raw(identifier_type_select_all)#[:2]  # slicing = return first two rows

#     # iterrating over the returned rows - will come in useful
#     for item in identifier_type.objects.raw(identifier_type_select_all):
#         print(str(item.id) + " " + item.type_name)

#     # mapping - might come in useful
#     identifier_types_map = {'id': 'id', 'identifier_type': 'type_name'}
#     objs = identifier_type.objects.raw(identifier_type_select_all, translations=identifier_types_map)
#     ident_type = objs[0].type_name # there has to be at least one result, or this will error

#     return render(request, "sandbox.html", {'data': data})


# def direct_sql_example(request):

#     data = dict_fetch(identifier_type_select_where_id, 2, [3])  # alternatively -  dict_fetch_one | dict_fetch_all

#     return render(request, "sandbox.html", {'data': data})


# # SERIALIZERS EXAMPLES
# @api_view(['GET', 'POST'])
# def api_identifier_types(request):

#     if request.method == 'GET':
#         data = dict_fetch_all(identifier_type_select_all)
#         serializer = IdentifierTypeSerializer(data, many=True)
#         return JsonResponse({"identifier_types": serializer.data}, safe=False)

#     elif request.method == 'POST':
#         serializer = IdentifierTypeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PUT', 'DELETE'])
# def api_identifier_type(request, id):
#     data = dict_fetch_one(identifier_type_select_where_id, [id])
#     if  not data:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         return JsonResponse({"identifier_type": data})

#     elif request.method == 'PUT':
#         serializer = CreateIdentifierTypeSerializer(data, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         delete_where(identifier_type_delete_where_id, [id])
#         # alternativelly via Django ORM:
#         # data = identifier_type.objects.get(pk=id)
#         # data.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # Using nested serializers/ nested JSON - tutorial:
# # https://www.youtube.com/watch?v=reDUKLuboI4


# # GENERIC VIEWS API EXAMPLES - DON'T WORK WITH RAW SQL
# class IdentifierTypesCR(generics.ListCreateAPIView): 
#     # queryset = dict_fetch_all(identifier_type_select_all) # does not update after put
#     # queryset = identifier_type.objects.all()  # alternative- Django ORM updates after PUT
#     queryset = identifier_type.objects.raw(identifier_type_select_all)  # does not update after put
#     serializer_class = IdentifierTypeSerializer

#     # overriding list method is not strictly necessary, but can be useful to put the data on a key
#     def list(self, request):
#         data = self.get_queryset()
#         serializer = IdentifierTypeSerializer(data, many=True)
#         return JsonResponse({"identifier_types": serializer.data}, safe=False)

# class IndentifierTypeRUD(generics.RetrieveUpdateDestroyAPIView):
#     queryset = dict_fetch_all(identifier_type_select_all) # doing it this way defeats the purpose of dict_fetch_one
#     serializer_class = IdentifierTypeSerializer
#     lookup_field = "id"
