# Generated by Django 4.2.5 on 2024-05-05 15:57

import apps.accounting.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("staticdata", "0001_initial"),
        ("classifiers", "0002_accounting_method_acrrual_type_asset_flow_type_and_more"),
        ("accounting", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="trade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("trader_id", models.SmallIntegerField(default=2)),
                (
                    "trade_datetime",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("bs_indicator", models.CharField(max_length=2)),
                (
                    "quantity",
                    models.FloatField(
                        validators=[apps.accounting.models.validate_greater_than_zero]
                    ),
                ),
                (
                    "price",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.0)]
                    ),
                ),
                (
                    "settlement_date",
                    models.DateTimeField(default=apps.accounting.models.t_plus_two),
                ),
                (
                    "trade_instrument_xrate",
                    models.FloatField(
                        default=1,
                        validators=[apps.accounting.models.validate_greater_than_zero],
                    ),
                ),
                (
                    "trade_setlement_xrate",
                    models.FloatField(
                        default=1,
                        validators=[apps.accounting.models.validate_greater_than_zero],
                    ),
                ),
                (
                    "gross_consideration",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.0)]
                    ),
                ),
                (
                    "settlement_base_xrate",
                    models.FloatField(
                        default=1,
                        validators=[apps.accounting.models.validate_greater_than_zero],
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "update_date",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "account",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="trade_account",
                        to="accounting.broker_account",
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="trade_book",
                        to="accounting.book",
                    ),
                ),
                (
                    "ccy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="trade_ccy",
                        to="classifiers.currency",
                    ),
                ),
                (
                    "counterparty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="trade_account",
                        to="staticdata.organization",
                    ),
                ),
                (
                    "instrument",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trade_instrument",
                        to="staticdata.instrument",
                    ),
                ),
                (
                    "settlement_ccy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="trade_settlement_ccy",
                        to="classifiers.currency",
                    ),
                ),
                (
                    "strategy",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="trade_strategy",
                        to="accounting.strategy",
                    ),
                ),
                (
                    "trade_status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="trade_status",
                        to="classifiers.trade_status",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="instrument_position",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "update_date",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "account",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="instrument_position_account",
                        to="accounting.broker_account",
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="instrument_position_book",
                        to="accounting.book",
                    ),
                ),
                (
                    "instrument",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="instrument_position_instrument",
                        to="staticdata.instrument",
                    ),
                ),
                (
                    "position_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="instrument_position_position_type",
                        to="classifiers.position_type",
                    ),
                ),
                (
                    "strategy",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="instrument_position_strategy",
                        to="accounting.strategy",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="cash_position",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "update_date",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "account",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cash_position_account",
                        to="accounting.broker_account",
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cash_position_book",
                        to="accounting.book",
                    ),
                ),
                (
                    "ccy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cash_position_ccy",
                        to="classifiers.currency",
                    ),
                ),
                (
                    "instrument_position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cash_position_instrument_position",
                        to="accounting.instrument_position",
                    ),
                ),
                (
                    "position_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cash_position_position_type",
                        to="classifiers.position_type",
                    ),
                ),
                (
                    "strategy",
                    models.ForeignKey(
                        default=2,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cash_position_strategy",
                        to="accounting.strategy",
                    ),
                ),
            ],
        ),
    ]