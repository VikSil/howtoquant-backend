from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .db.queries import equities_select_all
from howtoquant.utils import dict_fetch_all

import datetime as dt
import pandas as pd
import pandas_datareader as web


def index(request):
    """
    Function for the main landing page
    """

    return render(
        request,
        "index.html",
    )

@api_view(['GET'])
def all_equities(request):

    if request.method == 'GET':
        data = dict_fetch_all(equities_select_all)
        return JsonResponse({"equities": data}, safe=False)
