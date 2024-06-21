from .models import strategy, broker_account, book, trade
from apps.staticdata.models import organization, identifier
from apps.staticdata.utils import find_ultimate_owner_id, check_if_public
from apps.classifiers.models import accounting_method, currency, trade_status
from datetime import datetime

def get_base_ccy(book_name:str) ->str:
    book_obj = book.objects.get(name=book_name)
    return book_obj.base_ccy.ISO
    

def get_default_acct_name(book_name:str) -> str:
    book_obj = book.objects.get(name=book_name)
    return book_obj.default_account.account_name

def get_inst_ccy_by_ticker(ticker:str) ->str:
    inst_obj = identifier.objects.get(code = ticker).instrument
    return inst_obj.base_ccy.ISO


def save_book(
    name: str,
    acct_method: str,
    base_ccy: str,
    fund_name: str,
    default_account: str,
    external_name: str = '',
):
    method = accounting_method.objects.get(method_name=acct_method)
    ccy = currency.objects.get(ISO=base_ccy)
    parent_fund = organization.objects.get(short_name=fund_name)
    account = broker_account.objects.get(account_name=default_account)

    new_book = book.objects.create(
        name=name,
        external_name=external_name,
        accounting_method=method,
        base_ccy=ccy,
        fund_org=parent_fund,
        default_account=account,
    )
    return new_book


def save_pbaccount(
    name: str,
    cash_account: bool,
    broker_name: str,
    fund_name: str,
    external_name: str = '',
):

    parent_pb = organization.objects.get(short_name=broker_name)
    parent_fund = organization.objects.get(short_name=fund_name)
    # if either of the above do not exist, they will throw error upwards

    # find the PBs ultimate owner
    master_pb_id = find_ultimate_owner_id(parent_pb)
    is_pb_public = check_if_public(master_pb_id)
    # if PB's ultimate owner is not Public
    if not is_pb_public:
        master_fund_id = find_ultimate_owner_id(parent_fund)
        if (
            master_pb_id != master_fund_id
        ):  # make sure that Fund and PB have the same ultimate owner
            raise Exception('Different PB and Fund owners')

    new_account = broker_account.objects.create(
        account_name=name,
        fund_org=parent_fund,
        broker_org=parent_pb,
        external_name=external_name,
        cash_account=cash_account,
    )
    return new_account


def save_strategy(name: str, description: str = ''):
    new_strategy = strategy.objects.create(
        name=name,
        description=description,
        owner_org_id=9,  # to be replaced by user management
    )
    return new_strategy


def save_trade(
    ticker: str,
    direction: str,
    quantity: float,
    price: float,
    trade_ccy: str,
    settle_ccy: str,
    trade_settle_xrate: float,
    settle_base_xrate: float,
    book_name: str,
    strategy_name: str,
    account_name: str,
    counterparty: str,
    consideration:float,
    status: str = 'N',
    **kwargs
):

    trade_status_obj = trade_status.objects.get(code=status)
    instrument_obj = identifier.objects.get(code=ticker).instrument
    trade_ccy_obj = currency.objects.get(ISO=trade_ccy)
    settle_ccy_obj = currency.objects.get(ISO=settle_ccy)
    book_obj = book.objects.get(name=book_name)
    strategy_obj = strategy.objects.get(name=strategy_name)
    account_obj = broker_account.objects.get(account_name=account_name)
    counterparty_obj = organization.objects.get(short_name=counterparty)

    new_trade = trade.objects.create(
        trade_status=trade_status_obj,
        instrument=instrument_obj,
        bs_indicator=direction,
        quantity=quantity,
        price=price,
        ccy=trade_ccy_obj,
        settlement_ccy=settle_ccy_obj,
        trade_settlement_xrate=trade_settle_xrate,
        book=book_obj,
        strategy=strategy_obj,
        account=account_obj,
        counterparty=counterparty_obj,
        gross_consideration=consideration,
        settlement_base_xrate=settle_base_xrate,
    )
    if 'trade_date' in kwargs:
        new_trade.trade_datetime = kwargs['trade_date']
    if 'settle_date' in kwargs:
        new_trade.settlement_date = kwargs['settle_date']
    new_trade.save()

    return new_trade


def validate_trade_dates(trade_date: str, settlement_date: str) -> bool:
    '''
    Function validates trade and settlement dates and throws an error if not valid
    '''
    if len(trade_date) > 10:
        trade_dt = datetime.strptime(trade_date, '%Y-%m-%d %H:%M:%S')
    else:
        trade_dt = datetime.strptime(trade_date, '%Y-%m-%d')
    settle_dt = datetime.strptime(settlement_date, '%Y-%m-%d')
    if trade_dt > datetime.now():
        raise ValueError('Trade date in the future')
    if trade_dt > settle_dt:
        raise ValueError('Settlement date before trade date')
    return True


def verify_trade_book_account(book_name: str, account_name: str) -> bool:
    book_fund = book.objects.get(name=book_name).fund_org
    account_fund = broker_account.objects.get(account_name=account_name).fund_org
    return book_fund == account_fund