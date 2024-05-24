from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .db.queries import *
from .schemas import *
from .utils import *
from howtoquant.utils import dict_fetch_all, list_fetch_all

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


@api_view(['GET', 'POST'])
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

    elif request.method == 'POST':
        body = request.data
        try:
            validate(instance=body, schema=new_pbaccount)
        except ValidationError:
            return HttpResponseBadRequest('Request validation failed', status=400)

        try:
            pb_account = save_pbaccount(**{key: value for key, value in body.items() if value is not None})
            result = model_to_dict(pb_account)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Referenced organization does not exist', status=404)
        except Exception as e:
            result = str(e)
            status = 'NOK'
        else:
            status = 'OK'

        return JsonResponse({"data": result, 'status': status}, safe=False)


@api_view(['GET'])
def pbaccounts_names(request):
    if request.method == 'GET':
        data = list_fetch_all(pbaccounts_select_all_names)
        return JsonResponse({'status': "OK", 'data': {"method_names": data}}, safe=False)


@api_view(['GET', 'POST'])
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
    elif request.method == 'POST':
        body = request.data
        try:
            validate(instance=body, schema=new_strategy)
        except ValidationError:
            return HttpResponseBadRequest('Request validation failed', status=400)

        try:
            strategy = save_strategy(**{key: value for key, value in body.items() if value is not None})
            result = model_to_dict(strategy)
        except Exception as e:
            result = str(e)
            status = 'NOK'
        else:
            status = 'OK'

        return JsonResponse({"data": result, 'status': status}, safe=False)
