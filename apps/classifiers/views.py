from django.http import JsonResponse
from rest_framework.decorators import api_view
from howtoquant.utils import dict_fetch_all

from .db.queries import *


@api_view(['GET'])
def org_types(request):
    if request.method == 'GET':
        data = dict_fetch_all(organization_type_select_all)
        return JsonResponse({'status': "OK", 'data': {"org_types": data}}, safe=False)


@api_view(['GET'])
def inst_classes(request):
    if request.method == 'GET':
        data = dict_fetch_all(instrument_class_select_specified)
        return JsonResponse({'status': "OK", 'data': {"inst_classes": data}}, safe=False)


@api_view(['GET'])
def countries(request):
    if request.method == 'GET':
        data = dict_fetch_all(country_select_all)
        return JsonResponse({'status': "OK", 'data': {"countries": data}}, safe=False)


@api_view(['GET'])
def currencies(request):
    if request.method == 'GET':
        data = dict_fetch_all(currency_select_all)
        return JsonResponse({'status': "OK", 'data': {"currencies": data}}, safe=False)
