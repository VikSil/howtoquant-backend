import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .db.queries import *
from apps.classifiers.db.queries import (
    country_set_active_where_iso2,
    currency_set_active,
    country_select_all_names,
    currency_select_all_codes,
    identifier_type_select_all_names,
)
from apps.classifiers.models import country
from .schemas import *
from .utils_download import get_or_save_organization, save_equity, get_or_save_ticker
from howtoquant.utils import dict_fetch_all, dict_fetch_one, list_fetch_all, fetch_one_value, execute_where
from howtoquant.settings import POLYGON_API_KEY


def index(request):
    """
    Function for the main landing page
    """

    return render(
        request,
        "index.html",
    )


@api_view(['GET'])
def all_broker_names(request):
    data = list_fetch_all(organizations_select_all_broker_names)
    return JsonResponse({'status': "OK", 'data': {"broker_names": data}}, safe=False)


@api_view(['GET'])
def all_fund_names(request):
    data = list_fetch_all(organizations_select_all_fund_names)
    return JsonResponse({'status': "OK", 'data': {"fund_names": data}}, safe=False)


@api_view(['GET'])
def all_issuer_names(request):
    data = list_fetch_all(organizations_select_all_issuer_names)
    return JsonResponse({'status': "OK", 'data': {"issuer_names": data}}, safe=False)


@api_view(['GET'])
def all_identifier_codes(request):
    data = list_fetch_all(identifiers_select_all_codes)
    return JsonResponse({'status': "OK", 'data': {"codes": data}}, safe=False)


@api_view(['GET'])
def all_parent_org_names(request):
    data = list_fetch_all(organizations_select_all_parent_org_names)
    return JsonResponse({'status': "OK", 'data': {"org_names": data}}, safe=False)


@api_view(['GET'])
def equities(request, ticker=None):
    if request.method == 'GET':
        if ticker == None:  # list of all equities requested
            data = dict_fetch_all(equities_select_all)
            return JsonResponse({'status': "OK", 'data': {"equities": data}}, safe=False)
        else:  # specific equity requested by ticker
            inst_id = fetch_one_value(ticker_select_where_code, [ticker])
            if inst_id:
                data = dict_fetch_one(instruments_select_where_id, [inst_id])
                return JsonResponse({'status': "OK", 'data': {"instrument_data": data}}, safe=False)
            else:
                return HttpResponseBadRequest('Ticker Not Found', status=404)


@api_view(['GET'])
def identifiers(request):
    if request.method == 'GET':
        data = dict_fetch_all(identifiers_select_all)
        return JsonResponse({'status': "OK", 'data': {"identifiers": data}}, safe=False)


@api_view(['PUT', 'POST'])
def instruments(request):
    body = request.data
    print(body)

    if request.method == 'POST':  # save manually input instrument data
        try:
            validate(instance=body, schema=new_instrument)
        except ValidationError:
            return HttpResponseBadRequest('Request validation failed', status=400)

        country_name = body.get('domicile')
        print(country_name)
        ccy = body.get('ccy')
        ticker = body.get('ticker')
        ticker_type = body.get('ticker_type')

        if body.get('class_name') != 'Common Stock':
            result = 'Unsupported instrument type'
            status = 'NOK'
        elif country_name != None and country_name not in list_fetch_all(country_select_all_names, [1]):
            result = 'Domicile country not recognised'
            status = 'NOK'
        elif ccy != None and ccy not in list_fetch_all(currency_select_all_codes, [1]):
            result = 'Currency code not recognised'
            status = 'NOK'
        elif ticker_type != None and ticker_type not in list_fetch_all(identifier_type_select_all_names):
            result = 'Ticker type not recognised'
            status = 'NOK'

        try:
            inst_org = get_or_save_organization('Issuer', body.get('issuer_name'))
            country_obj = country.objects.get(short_name=country_name)
            print(country_obj)

            new_cs = save_equity(
                body.get('name'),
                inst_org,
                country_obj,
                ccy,
            )
            if ticker:
                inst_ticker = get_or_save_ticker(ticker, new_cs.instrument_id, type_name=ticker_type)
                ticker_id = inst_ticker.id
            else:
                ticker_id = None

        except Exception as e:
            status = 'NOK'
            result = str(e)

        else:
            result = {
                "organization": inst_org.id,
                "instrument_id": new_cs.instrument_id,
                "equity_id": new_cs.id,
                "ticker_id": ticker_id,
            }
            status = 'OK'

        return JsonResponse({"data": result, 'status': status}, safe=False)

    elif request.method == 'PUT':  # download new instrument from external API
        try:
            validate(instance=body, schema=new_instrument_request)
        except ValidationError:
            return HttpResponseBadRequest('Request validation failed', status=400)

        ticker = body['ticker']
        service = body['service']

        if service == 'polygon.io':
            try:
                url = f'https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_API_KEY}'
                response = requests.get(url)
                if response.status_code == 200:
                    if response.json().get('results').get('type') == 'CS':
                        inst_org = get_or_save_organization(
                            'Issuer',
                            response.json()['results']['name'],
                            response.json().get('results').get('description'),
                        )

                        ccy = response.json().get('results').get('currency_name')
                        country_iso2 = response.json().get('results').get('locale')
                        try:
                            country_obj = country.objects.get(ISO2=country_iso2)
                        except country.DoesNotExist:
                            country_obj = None

                        new_cs = save_equity(
                            response.json()['results']['name'],
                            inst_org,
                            country_obj,
                            ccy,
                            response.json().get('results').get('sic_description'),
                        )

                        activate_ccy = execute_where(currency_set_active, ccy)
                        activate_country = execute_where(country_set_active_where_iso2, country_iso2)

                        inst_ticker = get_or_save_ticker(ticker, new_cs.instrument_id)

                        result = {
                            "organization": inst_org.id,
                            "instrument_id": new_cs.instrument_id,
                            "equity_id": new_cs.id,
                            "ticker_id": inst_ticker.id,
                        }
                        status = 'OK'
                    else:
                        result = 'Unsupported instrument type'
                        status = 'NOK'
                elif response.json()['status'] == 'ERROR':
                    result = response.json()['error']
                    status = 'NOK'
                elif response.json()['status'] == 'NOT_FOUND':
                    result = response.json()['message']
                    status = 'NOK'
                else:
                    result = 'Unexpected error occured'
                    status = 'NOK'

            except Exception as e:
                result = str(e)
                status = 'NOK'

        return JsonResponse({"data": result, 'status': status}, safe=False)


@api_view(['GET', 'POST'])
def organizations(request):
    if request.method == 'GET':
        org_type_param = request.GET.get('org_type', None)
        try:
            if org_type_param != None:
                data = dict_fetch_all(organization_select_where_type, [org_type_param])
            else:
                data = dict_fetch_all(organization_select_all)
        except Exception as e:
            data = str(e)
            status = 'NOK'
        else:
            status = 'OK'

        return JsonResponse({"data": {"organizations": data}, 'status': status}, safe=False)

    elif request.method == 'POST':
        body = request.data
        try:
            validate(instance=body, schema=new_organization)
        except ValidationError:
            return HttpResponseBadRequest('Request validation failed', status=400)

        try:
            org = get_or_save_organization(
                **{key: value for key, value in body.items() if value is not None and value != ''}
            )
            result = model_to_dict(org)
        except Exception as e:
            result = str(e)
            status = 'NOK'
        else:
            status = 'OK'

        return JsonResponse({"data": result, 'status': status}, safe=False)
