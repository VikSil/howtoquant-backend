from django.db.models import Q

from .models import organization, equity, identifier, instrument
from apps.classifiers.models import (
    identifier_type,
    industry_sector,
    industry_subsector,
    instrument_class,
    country,
    currency,
    identifier_type,
    organization_type,
)


def get_or_save_organization(name: str, description: str):
    try:
        existing_org = organization.objects.get(Q(short_name=name) | Q(long_name=name))
    except organization.DoesNotExist:
        existing_org = None

    if existing_org:
        return existing_org

    else:
        new_organization = organization.objects.create(
            org_type=organization_type.objects.get(type_name='Issuer'),
            short_name=name[:25],
            long_name=name,
            description=description[:255],
            owner_org=organization.objects.get(pk=1),
        )
        new_organization.save()
        return new_organization


def save_equity(
    name: str,
    issuer: object,
    domicile: str = 'Unspecified',
    base_ccy: str = 'Unspecified',
    sector: str = 'Unspecified',
    subsector: str = 'Unspecified',
    inst_class: str = 'Common Stock',
):
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
        existing_equity = update_equity(existing_inst, sector=eq_sector, subsector = eq_subsector)
        return existing_equity

    else:  # insert new
        new_instrument = save_instrument(name, inst_class, domicile, base_ccy, issuer)
        new_equity = equity.objects.create(instrument=new_instrument, sector=eq_sector, subsector=eq_subsector)
        return new_equity


def save_instrument(name: str, inst_class: str, domicile: str, base_ccy: str, issuer: object):

    new_instrument = instrument.objects.create(
        name=name,
        short_name=name[:35],
        instrument_class=inst_class,
        domicile=country.objects.get(ISO2=domicile),
        base_ccy=currency.objects.get(ISO=base_ccy),
        issuer=issuer,
        owner_org=organization.objects.get(pk=1),
    )
    new_instrument.save()
    return new_instrument


def update_instrument(instrument: object, **kwargs):
    if 'domicile' in kwargs:
        instrument.domicile = country.objects.get(ISO2=kwargs.get('domicile'))
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
    new_sector.save()
    return new_sector


def save_industry_subsector(name: str, sector: object):
    new_subsector = industry_subsector.objects.create(subsector_name=name[:255], sector=sector)
    new_subsector.save()
    return new_subsector
