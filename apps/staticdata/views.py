from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .db.queries import equities_select_all, identifiers_select_all, identifiers_select_all_codes
from howtoquant.utils import dict_fetch_all, list_fetch_all


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


@api_view(['GET'])
def all_identifiers(request):

    if request.method == 'GET':
        data = dict_fetch_all(identifiers_select_all)
        return JsonResponse({"identifiers": data}, safe=False)

@api_view(['GET'])
def all_identifier_codes(request):

    data = list_fetch_all(identifiers_select_all_codes)
    return JsonResponse({"codes": data}, safe=False)
