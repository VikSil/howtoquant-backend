from django.db.models import Q

from .models import organization, equity, identifier, instrument
from apps.classifiers.models import (
    industry_sector,
    industry_subsector,
    instrument_class,
    country,
    currency,
    organization_type,
    identifier_type,
)


def get_org_by_name_and_type(name: str, **kwargs):
    try:
        if 'org_type' in kwargs:  # if org_type is stated, use it in query
            existing_org = organization.objects.filter(
                org_type__in=organization_type.objects.filter(type_name__in=kwargs['org_type'])
            ).get(Q(short_name=name) | Q(long_name=name))
        else:  # if org_type is not stated, query by name only

            existing_org = organization.objects.get(Q(short_name=name) | Q(long_name=name))
    except organization.DoesNotExist:
        existing_org = None

    return existing_org


def get_or_save_organization(org_type: str, name: str, description: str = '', **kwargs):
    existing_org = get_org_by_name_and_type(name, org_type=[org_type])
    if existing_org:
        return existing_org

    else:
        owner_org = None
        if 'owner_org' in kwargs:  # if owner org explicitly stated
            owner_org_type = ['Headquarters', 'Fund']  # if owner org type not stated, assume values
            if 'owner_org_type' in kwargs:  # or use explicitly stated owner org type
                owner_org_type = kwargs['owner_org_type']
            owner_org = get_org_by_name_and_type(name=kwargs['owner_org'], org_type=owner_org_type)  # find owner org
        if not owner_org:  # if owner org not known
            if org_type in ['Fund', 'Book', 'Strategy']:  # for these types the owner is user's headquarters
                owner_org = get_org_by_name_and_type(name='Silver Pine', org_type=['Headquarters'])
            else:
                owner_org = organization.objects.get(pk=1)  # default the new org to Public Domain

        new_org = organization(
            org_type=organization_type.objects.get(type_name=org_type),
            short_name=name[:25],
            long_name=name,
            description=description[:255],
            owner_org=owner_org,
        )
        if 'long_name' in kwargs:
            new_org.long_name = kwargs.get('long_name')

        new_org.save()
        return new_org


def get_or_save_ticker(ticker: str, inst_id: int, type_name: str = 'BBG Ticker'):
    try:
        existing_ticker = identifier.objects.get(code=ticker)
    except identifier.DoesNotExist:
        existing_ticker = None

    if existing_ticker:
        return existing_ticker
    else:
        new_ticker = identifier.objects.create(
            code=ticker,
            identifier_type=identifier_type.objects.get(type_name=type_name),
            instrument=instrument.objects.get(pk=inst_id),
        )
        return new_ticker


def save_equity(
    name: str,
    issuer: object,
    domicile: object,
    base_ccy: str = 'Unspecified',
    sector: str = 'Unspecified',
    subsector: str = 'Unspecified',
    inst_class: str = 'Common Stock',
):
    if not domicile:
        domicile = country.objects.get(short_name='Unspecified')
    inst_class = instrument_class.objects.get(instrument_class=inst_class)

    if len(sector) > 0:
        try:
            eq_sector = industry_sector.objects.get(sector_name=sector)
        except industry_sector.DoesNotExist:
            eq_sector = save_industry_sector(sector)
    else:
        eq_sector = industry_sector.objects.get(sector_name='Unspecified')

    if len(subsector) > 0:
        try:
            eq_subsector = industry_subsector.objects.get(subsector_name=subsector)
        except industry_subsector.DoesNotExist:
            eq_subsector = save_industry_subsector(subsector, eq_sector)
    else:
        eq_subsector = industry_subsector.objects.get(subsector_name='Unspecified')

    try:
        existing_inst = instrument.objects.get(Q(short_name=name) | Q(name=name))
    except instrument.DoesNotExist:
        existing_inst = None

    if existing_inst:  # update
        existing_inst = update_instrument(existing_inst, domicile=domicile, base_ccy=base_ccy, issuer=issuer)
        existing_equity = update_equity(existing_inst, sector=eq_sector, subsector=eq_subsector)
        return existing_equity

    else:  # insert new
        new_instrument = save_instrument(name, inst_class, domicile, base_ccy, issuer)
        new_equity = equity.objects.create(instrument=new_instrument, sector=eq_sector, subsector=eq_subsector)
        return new_equity


def save_instrument(name: str, inst_class: str, domicile: object, base_ccy: str, issuer: object):

    new_instrument = instrument.objects.create(
        name=name,
        short_name=name[:35],
        instrument_class=inst_class,
        domicile=domicile,
        base_ccy=currency.objects.get(ISO=base_ccy),
        issuer=issuer,
        owner_org=organization.objects.get(pk=1),
    )
    return new_instrument


def update_instrument(instrument: object, **kwargs):
    if 'domicile' in kwargs:
        instrument.domicile = kwargs.get('domicile')
    if 'base_ccy' in kwargs:
        instrument.base_ccy = currency.objects.get(ISO=kwargs.get('base_ccy'))
    if 'issuer' in kwargs:
        instrument.issuer = kwargs.get('issuer')
    instrument.save()
    return instrument


def update_equity(parent_inst: object, **kwargs):

    equity_row = equity.objects.get(instrument=parent_inst.id)
    if 'sector' in kwargs:
        equity_row.sector = kwargs.get('sector')
    if 'subsector' in kwargs:
        equity_row.subsector = kwargs.get('subsector')
    if 'dividend_frequency' in kwargs:
        equity_row.dividend_frequency = kwargs.get('dividend_frequency')
    equity_row.save()
    return equity_row


def save_industry_sector(name: str):
    new_sector = industry_sector.objects.create(sector_name=name[:100])
    return new_sector


def save_industry_subsector(name: str, sector: object):
    new_subsector = industry_subsector.objects.create(subsector_name=name[:255], sector=sector)
    return new_subsector
