from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import datetime as dt


from .schemas import new_price_request, download_save_request
from .utils_download import download_market_data
from .db.queries import download_data_select_prices, price_ladder_select_all, save_download_prices_proc
from howtoquant.utils import dict_fetch_all, trigger_proc

def index(request):
    """
    Function for the main landing page
    """

    return render(
        request,
        "marketdata/index.html",
    )


@api_view(['GET'])
def get_prices(request):
    data = dict_fetch_all(price_ladder_select_all)
    return JsonResponse({"prices": data}, safe=False)

@api_view(['PUT'])
def put_prices(request):

    if request.method == 'PUT':
        body = request.data

        try:
            validate(instance=body, schema=new_price_request)

        except ValidationError as e:
            return HttpResponseBadRequest('Request validation failed', status=400)

        tickers = body['tickers']
        start_dt = dt.datetime.strptime(body['date_from'], '%Y-%m-%d').date()
        end_dt = dt.datetime.strptime(body['date_to'], '%Y-%m-%d').date()

        download_id = download_market_data('Yahoo Finance Prices', tickers, start_dt, end_dt)

        return JsonResponse({"download_id": download_id}, safe=False)


@api_view(['GET'])
def get_download_prices(request, download_id):
    data = dict_fetch_all(download_data_select_prices, [download_id])
    if data:
        for price in data:
            price['bid_price'] = round(price['bid_price'],2)
            price['ask_price'] = round(price['ask_price'],2)
        return JsonResponse({"prices": data}, safe=False)
    else:
        return HttpResponseBadRequest('Download Not Found', status=404)

@api_view(['PUT'])
def put_download_prices(request):
    body =request.data

    try:
        validate(instance=body, schema = download_save_request)
    except ValidationError as e:
        return HttpResponseBadRequest('Request validation failed', status=400)

    download_id = body['download_id']
    if body['options'] == 'missing':
        options = 0 # only fill out missing values
    else:
        options = 1 # save and override all
    result = trigger_proc(save_download_prices_proc, [download_id, options])
    return JsonResponse({"result": result}, safe=False)
