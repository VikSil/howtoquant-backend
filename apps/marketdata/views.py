from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from jsonschema import validate
from jsonschema.exceptions import ValidationError

import json
import datetime as dt
import pandas as pd
from pandas_datareader import data as web
import yfinance as yfin

from .schemas import new_price_request

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

    if request.method == 'GET':
        body = request.data

        try:
            validate(instance=body, schema=new_price_request)

        except ValidationError as e:
            return HttpResponseBadRequest('Request validation failed', status=400)

        ticker = body['ticker']
        start_dt = dt.datetime.strptime(body['date_from'], '%Y-%m-%d').date()
        end_dt = dt.datetime.strptime(body['date_to'], '%Y-%m-%d').date()

        yfin.pdr_override()
        df = web.get_data_yahoo(ticker, start=start_dt, end=end_dt)
        # truncate decimals to two places, Yahoo has 10
        df_json = df.to_json(double_precision=2, date_format='iso')  

        return JsonResponse({"prices": json.loads(df_json)}, safe=False)
