from django.db.models import Q

from .models import strategy, broker_account
from apps.staticdata.models import organization
from apps.staticdata.utils import find_ultimate_owner_id, check_if_public


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
