from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import copy

from .db.queries import *
from .schemas import *
from .utils import *
from howtoquant.utils import dict_fetch_all, list_fetch_all, dict_fetch_one
from apps.staticdata.utils_download import get_org_by_name_and_type, get_or_save_organization

# Create your views here.


def index(request):
    """
    Function for the main landing page
    """

    return render(
        request,
        "accounting/index.html",
    )


@api_view(['GET', 'POST'])
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
    elif request.method == 'POST':
        body = request.data
        try:
            validate(instance=body, schema=new_book)
        except ValidationError:
            return HttpResponseBadRequest('Request validation failed', status=400)

        try:
            book = save_book(
                **{key: value for key, value in body.items() if value is not None}
            )
            result = model_to_dict(book)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest(
                'Referenced organization does not exist', status=404
            )
        except Exception as e:
            result = str(e)
            status = 'NOK'
        else:
            status = 'OK'

        return JsonResponse({"data": result, 'status': status}, safe=False)


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
        return JsonResponse(
            {'status': status, 'data': {"pbaccounts": data}}, safe=False
        )

    elif request.method == 'POST':
        body = request.data
        try:
            validate(instance=body, schema=new_pbaccount)
        except ValidationError:
            return HttpResponseBadRequest('Request validation failed', status=400)

        try:
            pb_account = save_pbaccount(
                **{key: value for key, value in body.items() if value is not None}
            )
            result = model_to_dict(pb_account)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest(
                'Referenced organization does not exist', status=404
            )
        except Exception as e:
            result = str(e)
            status = 'NOK'
        else:
            status = 'OK'

        return JsonResponse({"data": result, 'status': status}, safe=False)


@api_view(['GET'])
def pbaccounts_names(request):
    if request.method == 'GET':
        fund_name = request.GET.get(
            'fund_name', 'Silver Pine'
        )  # use users headquarters
        data = list_fetch_all(pbaccounts_select_all_names, [fund_name])
        return JsonResponse(
            {'status': "OK", 'data': {"account_names": data}}, safe=False
        )


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
        return JsonResponse(
            {'status': status, 'data': {"strategies": data}}, safe=False
        )
    elif request.method == 'POST':
        body = request.data
        try:
            validate(instance=body, schema=new_strategy)
        except ValidationError:
            return HttpResponseBadRequest('Request validation failed', status=400)

        try:
            strategy = save_strategy(
                **{key: value for key, value in body.items() if value is not None}
            )
            result = model_to_dict(strategy)
        except Exception as e:
            result = str(e)
            status = 'NOK'
        else:
            status = 'OK'

        return JsonResponse({"data": result, 'status': status}, safe=False)


@api_view(['GET', 'POST'])
def trades(request, id = None):
    if request.method == 'GET':
        if id == None: # list of all trades requested
            try:
                data = dict_fetch_all(trades_select_all)
            except Exception as e:
                data = str(e)
                status = 'NOK'
            else:
                status = 'OK'
            return JsonResponse(
                {'status': status, 'data': {"trades": data}}, safe=False
            )
        else: #specific trade data requested
            data = dict_fetch_one(trades_select_where_id, [id])
            if data:
                return JsonResponse({'status': "OK", 'data':{'trade_data':data}}, safe=False)
            else:
                return HttpResponseBadRequest('Trade Not Found', status=404)
            
    elif request.method == 'POST':
        trade_data = copy.deepcopy(request.data)
        try:
            validate(instance=trade_data, schema=new_trade)
        except ValidationError:
            return HttpResponseBadRequest('Request validation failed', status=400)
        
        if ('trade_date' in trade_data) and ('settle_date' in trade_data):
            try:
                validate_trade_dates(trade_data['trade_date'], trade_data['settle_date'])
            except ValueError as e:
                return JsonResponse({"data": str(e), 'status': 'NOK'}, safe=False)
        
        if 'account_name' in trade_data:
            if not verify_trade_book_account(trade_data['book_name'], trade_data['account_name']):
                return JsonResponse({"data": 'Book and account belong to different funds', 'status': 'NOK'}, safe=False)
        else:
            trade_data['account_name'] = get_default_acct_name(trade_data['book_name'])
            
        if 'trade_ccy' not in trade_data:
            trade_data['trade_ccy'] = get_inst_ccy_by_ticker(trade_data['ticker'])
        if 'settle_ccy' not in trade_data:
            trade_data['settle_ccy'] = trade_data['trade_ccy']
        if trade_data['trade_ccy'] == trade_data['settle_ccy']:
            trade_data['trade_settle_xrate'] = 1
        elif 'trade_settle_xrate' not in trade_data:
            return JsonResponse({"data": 'FX rate needs to be specified for different trade and settlement currencies', "status": 'NOK'}, safe=False)
        
        base_ccy = get_base_ccy(trade_data['book_name'])
        if trade_data['settle_ccy'] != base_ccy:
            if 'settle_base_xrate' not in trade_data:
                return JsonResponse({"data": 'FX rate needs to be specified for different settlement and base currencies', "status": 'NOK'}, safe=False)
        
        if 'settle_base_xrate' not in trade_data:
            trade_data['settle_base_xrate']=1        
        
        if not get_org_by_name_and_type(trade_data['counterparty'], org_type = 'Counterparty'):
            get_or_save_organization(org_type = 'Counterparty', name = trade_data['counterparty'], description= 'New trade counterparty')
        
        trade_data['consideration'] = trade_data['price'] * trade_data['quantity']
        
        try:
            trade = save_trade(
                **{key: value for key, value in trade_data.items() if value is not None}
            )
            
            result = model_to_dict(trade)
        except Exception as e:
            result = str(e)
            status = 'NOK'
        else:
            status = 'OK'
        
        return JsonResponse({"data": result, 'status': status}, safe=False)