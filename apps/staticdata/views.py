import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.db.models.query import QuerySet
from rest_framework.decorators import api_view
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .db.queries import (
    equities_select_all,
    identifiers_select_all,
    identifiers_select_all_codes,
    instruments_select_where_id,
    ticker_select_where_code,
)
from .schemas import *
from .utils_download import get_or_save_organization, save_equity, get_or_save_ticker
from howtoquant.utils import dict_fetch_all, dict_fetch_one, list_fetch_all, fetch_one_value
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


@api_view(['GET'])
def all_identifier_codes(request):
    data = list_fetch_all(identifiers_select_all_codes)
    return JsonResponse({'status': "OK", 'data': {"codes": data}}, safe=False)


@api_view(['PUT'])
def instruments(request):
    body = request.data

    try:
        validate(instance=body, schema=new_instrument_request)
    except ValidationError as e:
        return HttpResponseBadRequest('Request validation failed', status=400)

    ticker = body['ticker']
    service = body['service']

    if service == 'polygon.io':
        try:
            url = f'https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_API_KEY}'
            response = requests.get(url)
            if response.status_code == 200:
                if response.json()['results']['type'] == 'CS':
                    inst_org = get_or_save_organization(
                        response.json()['results']['name'], response.json()['results']['description']
                    )

                    new_cs = save_equity(
                        response.json()['results']['name'],
                        inst_org,
                        response.json()['results']['locale'],
                        response.json()['results']['currency_name'],
                        response.json()['results']['sic_description'],
                    )

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
