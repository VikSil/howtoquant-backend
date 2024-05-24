from .models import strategy, broker_account, book
from apps.staticdata.models import organization
from apps.staticdata.utils import find_ultimate_owner_id, check_if_public
from apps.classifiers.models import accounting_method, currency


def save_book(
    name: str, acct_method: str, base_ccy: str, fund_name: str, default_account: str, external_name: str = ''
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
        if master_pb_id != master_fund_id:  # make sure that Fund and PB have the same ultimate owner
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
        name=name, description=description, owner_org_id=9  # to be replaced by user management
    )
    return new_strategy
