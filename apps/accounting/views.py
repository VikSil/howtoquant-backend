from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .db.queries import *
from howtoquant.utils import dict_fetch_all

# Create your views here.


def index(request):
    """
    Function for the main landing page
    """

    return render(
        request,
        "accounting/index.html",
    )


@api_view(['GET'])
def books(request):
    if request.method == 'GET':
        try:
            data = dict_fetch_all(books_select_all)
        except Exception as e:
            data = str(e)
            status = 'NOK'
        else:
            status = 'OK'
        return JsonResponse({'status': status, 'data': {"books": data}}, safe=False)


@api_view(['GET'])
def strategies(request):
    if request.method == 'GET':
        try:
            data = dict_fetch_all(strategies_select_all)
        except Exception as e:
            data = str(e)
            status = 'NOK'
        else:
            status = 'OK'
        return JsonResponse({'status': status, 'data': {"strategies": data}}, safe=False)


@api_view(['GET'])
def pbaccounts(request):
    if request.method == 'GET':
        try:
            data = dict_fetch_all(pbaccounts_select_all)
        except Exception as e:
            data = str(e)
            status = 'NOK'
        else:
            status = 'OK'
        return JsonResponse({'status': status, 'data': {"pbaccounts": data}}, safe=False)
