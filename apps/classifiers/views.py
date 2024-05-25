from django.http import JsonResponse
from rest_framework.decorators import api_view
from howtoquant.utils import dict_fetch_all, list_fetch_all

from .db.queries import *


@api_view(['GET'])
def accounting_method_names(request):
    if request.method == 'GET':
        data = list_fetch_all(accounting_method_select_all_names)
        return JsonResponse({'status': "OK", 'data': {"method_names": data}}, safe=False)


@api_view(['GET'])
def countries(request):
    if request.method == 'GET':
        active_param = request.GET.get('active', 1)
        data = dict_fetch_all(country_select_all, [active_param])
        return JsonResponse({'status': "OK", 'data': {"countries": data}}, safe=False)


@api_view(['GET'])
def country_names(request):
    if request.method == 'GET':
        active_param = request.GET.get('active', 1)
        data = list_fetch_all(country_select_all_names, [active_param])
        return JsonResponse({'status': "OK", 'data': {"country_names": data}}, safe=False)


@api_view(['GET'])
def currencies(request):
    if request.method == 'GET':
        active_param = request.GET.get('active', 1)
        data = dict_fetch_all(currency_select_all, [active_param])
        return JsonResponse({'status': "OK", 'data': {"currencies": data}}, safe=False)


@api_view(['GET'])
def currency_codes(request):
    if request.method == 'GET':
        active_param = request.GET.get('active', 1)
        data = list_fetch_all(currency_select_all_codes, [active_param])
        return JsonResponse({'status': "OK", 'data': {"ccy_codes": data}}, safe=False)


@api_view(['GET'])
def inst_classes(request):
    if request.method == 'GET':
        data = dict_fetch_all(instrument_class_select_specified)
        return JsonResponse({'status': "OK", 'data': {"inst_classes": data}}, safe=False)


@api_view(['GET'])
def inst_class_names(request):
    if request.method == 'GET':
        data = list_fetch_all(instrument_class_select_all_names)
        return JsonResponse({'status': "OK", 'data': {"class_names": data}}, safe=False)


@api_view(['GET'])
def org_types(request):
    if request.method == 'GET':
        data = dict_fetch_all(organization_type_select_all)
        return JsonResponse({'status': "OK", 'data': {"org_types": data}}, safe=False)


@api_view(['GET'])
def sectors(request):
    if request.method == 'GET':
        data = dict_fetch_all(industry_sector_select_all)
        return JsonResponse({'status': "OK", 'data': {"sectors": data}}, safe=False)


@api_view(['GET'])
def subsectors(request):
    if request.method == 'GET':
        data = dict_fetch_all(industry_subsector_select_all)
        return JsonResponse({'status': "OK", 'data': {"subsectors": data}}, safe=False)


@api_view(['GET'])
def ticker_types(request):
    if request.method == 'GET':
        data = dict_fetch_all(identifier_type_select_specified)
        return JsonResponse({'status': "OK", 'data': {"ticker_types": data}}, safe=False)
