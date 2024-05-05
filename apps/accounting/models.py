from django.db import models
from django.utils.timezone import now, timedelta
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


def t_plus_two():
    return now() + timedelta(days=2)


def validate_greater_than_zero(value):
    if value <= 0:
        raise ValidationError(
            _("%(value)s is not greater than zero."),
            params={"value": value},
        )


class broker_account(models.Model):
    account_name = models.CharField(max_length=100)
    fund_org = models.ForeignKey('staticdata.organization', on_delete=models.PROTECT, related_name='account_fund')
    broker_org = models.ForeignKey('staticdata.organization', on_delete=models.PROTECT, related_name='account_broker')
    external_name = models.CharField(max_length=100, blank=True, null=True)
    cash_account = models.BooleanField(blank=False, null=False, default=False)
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class book(models.Model):
    fund_org = models.ForeignKey('staticdata.organization', on_delete=models.PROTECT, related_name='book_fund')
    name = models.CharField(max_length=100)
    default_account_id = models.ForeignKey(
        broker_account, on_delete=models.SET_DEFAULT, default=2, related_name='book_default_account'
    )
    external_name = models.CharField(max_length=100, blank=True, null=True)
    accounting_method = models.ForeignKey('classifiers.accounting_method', on_delete=models.PROTECT)
    base_ccy = models.ForeignKey('classifiers.currency', on_delete=models.PROTECT, related_name='book_ccy')
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class strategy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    owner_org = models.ForeignKey('staticdata.organization', on_delete=models.PROTECT, related_name='strategy_owner')
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class trade(models.Model):
    trader_id = models.SmallIntegerField(default=2)
    trade_datetime = models.DateTimeField(default=now)
    trade_status = models.ForeignKey('classifiers.trade_status', on_delete=models.PROTECT, related_name='trade_status')
    instrument = models.ForeignKey('staticdata.instrument', on_delete=models.CASCADE, related_name='trade_instrument')
    bs_indicator = models.CharField(max_length=2)
    quantity = models.FloatField(unique=False, validators=[validate_greater_than_zero])
    price = models.FloatField(unique=False, validators=[MinValueValidator(0.0)])
    ccy = models.ForeignKey('classifiers.currency', on_delete=models.PROTECT, related_name='trade_ccy')
    settlement_date = models.DateTimeField(default=t_plus_two)
    settlement_ccy = models.ForeignKey(
        'classifiers.currency', on_delete=models.PROTECT, related_name='trade_settlement_ccy'
    )
    trade_instrument_xrate = models.FloatField(unique=False, validators=[validate_greater_than_zero], default=1)
    trade_setlement_xrate = models.FloatField(unique=False, validators=[validate_greater_than_zero], default=1)
    book = models.ForeignKey(book, on_delete=models.PROTECT, default=2, related_name='trade_book')
    strategy = models.ForeignKey(strategy, on_delete=models.PROTECT, default=2, related_name='trade_strategy')
    account = models.ForeignKey(broker_account, on_delete=models.PROTECT, default=2, related_name='trade_account')
    counterparty = models.ForeignKey('staticdata.organization', on_delete=models.PROTECT, related_name='trade_account')
    gross_consideration = models.FloatField(unique=False, validators=[MinValueValidator(0.0)])
    settlement_base_xrate = models.FloatField(unique=False, validators=[validate_greater_than_zero], default=1)
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class instrument_position(models.Model):
    instrument = models.ForeignKey(
        'staticdata.instrument', on_delete=models.CASCADE, related_name='instrument_position_instrument'
    )
    book = models.ForeignKey(book, on_delete=models.PROTECT, default=2, related_name='instrument_position_book')
    account = models.ForeignKey(
        broker_account, on_delete=models.PROTECT, default=2, related_name='instrument_position_account'
    )
    strategy = models.ForeignKey(
        strategy, on_delete=models.PROTECT, default=2, related_name='instrument_position_strategy'
    )
    position_type = models.ForeignKey(
        'classifiers.position_type', on_delete=models.PROTECT, related_name='instrument_position_position_type'
    )
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class cash_position(models.Model):
    ccy = models.ForeignKey('classifiers.currency', on_delete=models.PROTECT, related_name='cash_position_ccy')
    book = models.ForeignKey(book, on_delete=models.PROTECT, default=2, related_name='cash_position_book')
    account = models.ForeignKey(
        broker_account, on_delete=models.PROTECT, default=2, related_name='cash_position_account'
    )
    strategy = models.ForeignKey(strategy, on_delete=models.PROTECT, default=2, related_name='cash_position_strategy')
    position_type = models.ForeignKey(
        'classifiers.position_type', on_delete=models.PROTECT, related_name='cash_position_position_type'
    )
    instrument_position = models.ForeignKey(
        instrument_position, on_delete=models.CASCADE, related_name='cash_position_instrument_position'
    )
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class accrual_ladder(models.Model):
    instrument_position = models.ForeignKey(
        instrument_position, on_delete=models.CASCADE, related_name='accrual_ladder_instrument_position'
    )
    date = models.DateTimeField(default=now)
    accrual_type = models.ForeignKey(
        'classifiers.accrual_type', on_delete=models.PROTECT, related_name='accrual_ladder_accrual_type'
    )
    today_quantity = models.FloatField(unique=False)
    cumulative_quantity = models.FloatField(unique=False)
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class asset_flow(models.Model):
    position_id = models.PositiveBigIntegerField()
    source = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    source_fk = GenericForeignKey('source', 'position_id')
    trade_date = models.DateTimeField(default=now)
    settlement_date = models.DateTimeField(default=t_plus_two)
    quantity = models.FloatField(unique=False)
    price = models.FloatField(unique=False, validators=[MinValueValidator(0.0)])
    asset_flow_type = models.ForeignKey(
        'classifiers.asset_flow_type', on_delete=models.PROTECT, related_name='asset_flow_flow_type'
    )
    ccy = models.ForeignKey('classifiers.currency', on_delete=models.PROTECT, related_name='asset_flow_ccy')
    xrate = models.FloatField(unique=False, validators=[validate_greater_than_zero], default=1)
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class cash_ladder(models.Model):
    position = models.ForeignKey(cash_position, on_delete=models.CASCADE, related_name='cash_ladder_cash_position')
    date = models.DateTimeField(default=now)
    quantity = models.FloatField(unique=False)
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class asset_ladder(models.Model):
    position = models.ForeignKey(
        instrument_position, on_delete=models.CASCADE, related_name='asset_ladder_instrument_position'
    )
    date = models.DateTimeField(default=now)
    quantity = models.FloatField(unique=False)
    market_value = models.FloatField(unique=False)
    market_price = models.FloatField(unique=False)
    value_scheme_id = models.ForeignKey(
        'marketdata.value_scheme', on_delete=models.PROTECT, related_name='asset_ladder_value_scheme'
    )
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class weighted_pnl(models.Model):
    asset_ladder = models.ForeignKey(asset_ladder, on_delete=models.CASCADE, related_name='weighted_pnl_asset_ladder')
    average_cost = models.FloatField(unique=False)
    lifetime_total_pnl = models.FloatField(unique=False)
    lifetime_instrument_pnl = models.FloatField(unique=False)
    lifetime_fx_pnl = models.FloatField(unique=False)
    ytd_total_pnl = models.FloatField(unique=False)
    ytd_instrument_pnl = models.FloatField(unique=False)
    ytd_fx_pnl = models.FloatField(unique=False)
    mtd_total_pnl = models.FloatField(unique=False)
    mtd_instrument_pnl = models.FloatField(unique=False)
    mtd_fx_pnl = models.FloatField(unique=False)
    daily_total_pnl = models.FloatField(unique=False)
    daily_instrument_pnl = models.FloatField(unique=False)
    daily_fx_pnl = models.FloatField(unique=False)
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class fifo_pnl(models.Model):
    asset_ladder = models.ForeignKey(asset_ladder, on_delete=models.CASCADE, related_name='fifo_pnl_asset_ladder')
    average_cost = models.FloatField(unique=False)
    lifetime_total_pnl = models.FloatField(unique=False)
    lifetime_instrument_pnl = models.FloatField(unique=False)
    lifetime_fx_pnl = models.FloatField(unique=False)
    ytd_total_pnl = models.FloatField(unique=False)
    ytd_instrument_pnl = models.FloatField(unique=False)
    ytd_fx_pnl = models.FloatField(unique=False)
    mtd_total_pnl = models.FloatField(unique=False)
    mtd_instrument_pnl = models.FloatField(unique=False)
    mtd_fx_pnl = models.FloatField(unique=False)
    daily_total_pnl = models.FloatField(unique=False)
    daily_instrument_pnl = models.FloatField(unique=False)
    daily_fx_pnl = models.FloatField(unique=False)
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)


class position_snapshot(models.Model):
    position_id = models.PositiveBigIntegerField()
    source = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name = 'position_snapshot_source')
    source_fk = GenericForeignKey('source', 'position_id')
    date = models.DateTimeField(default=now)
    quantity = models.FloatField(unique=False)
    market_value = models.FloatField(unique=False)
    market_price = models.FloatField(unique=False)
    value_scheme_id = models.ForeignKey(
        'marketdata.value_scheme', on_delete=models.PROTECT, related_name='position_snapshot_value_scheme'
    )
    ladder_id = models.PositiveBigIntegerField()
    source_ladder = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='position_snapshot_source_ladder')
    source_ladder_fk = GenericForeignKey('source_ladder', 'ladder_id')
    weighted_average_cost = models.FloatField(unique=False)
    weighted_lifetime_total_pnl = models.FloatField(unique=False)
    weighted_lifetime_instrument_pnl = models.FloatField(unique=False)
    weighted_lifetime_fx_pnl = models.FloatField(unique=False)
    weighted_ytd_total_pnl = models.FloatField(unique=False)
    weighted_ytd_instrument_pnl = models.FloatField(unique=False)
    weighted_ytd_fx_pnl = models.FloatField(unique=False)
    weighted_mtd_total_pnl = models.FloatField(unique=False)
    weighted_mtd_instrument_pnl = models.FloatField(unique=False)
    weighted_mtd_fx_pnl = models.FloatField(unique=False)
    weighted_daily_total_pnl = models.FloatField(unique=False)
    weighted_daily_instrument_pnl = models.FloatField(unique=False)
    weighted_daily_fx_pnl = models.FloatField(unique=False)
    fifo_average_cost = models.FloatField(unique=False)
    fifo_lifetime_total_pnl = models.FloatField(unique=False)
    fifo_lifetime_instrument_pnl = models.FloatField(unique=False)
    fifo_lifetime_fx_pnl = models.FloatField(unique=False)
    fifo_ytd_total_pnl = models.FloatField(unique=False)
    fifo_ytd_instrument_pnl = models.FloatField(unique=False)
    fifo_ytd_fx_pnl = models.FloatField(unique=False)
    fifo_mtd_total_pnl = models.FloatField(unique=False)
    fifo_mtd_instrument_pnl = models.FloatField(unique=False)
    fifo_mtd_fx_pnl = models.FloatField(unique=False)
    fifo_daily_total_pnl = models.FloatField(unique=False)
    fifo_daily_instrument_pnl = models.FloatField(unique=False)
    fifo_daily_fx_pnl = models.FloatField(unique=False)
    created_date = models.DateTimeField(default=now, blank=True, unique=False)
    update_date = models.DateTimeField(default=now, blank=True, unique=False)
