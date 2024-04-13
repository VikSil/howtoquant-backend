from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from jsonschema import validate
from jsonschema.exceptions import ValidationError

import json
import datetime as dt
from pandas_datareader import data as web
import yfinance as yfin

from .schemas import new_price_request
from .utils_download import download_spec

def index(request):
    """
    Function for the main landing page
    """

    return render(
        request,
        "marketdata/index.html",
    )


@api_view(['PUT'])
def get_prices(request):

    if request.method == 'PUT':
        body = request.data

        try:
            validate(instance=body, schema=new_price_request)

        except ValidationError as e:
            return HttpResponseBadRequest('Request validation failed', status=400)

        tickers = body['tickers']
        start_dt = dt.datetime.strptime(body['date_from'], '%Y-%m-%d').date()
        end_dt = dt.datetime.strptime(body['date_to'], '%Y-%m-%d').date()

        download_id = download_spec(1, tickers, start_dt, end_dt)

        return JsonResponse({"download_id": download_id}, safe=False)
