# Generated by Django 4.2.5 on 2024-04-12 20:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("staticdata", "0006_rename_instrument_id_equity_instrument_and_more"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("classifiers", "0003_rename_ccy_id_country_ccy_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="download",
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
                ("start_datetime", models.DateTimeField(auto_now_add=True)),
                ("complete_datetime", models.DateTimeField(blank=True, null=True)),
                ("requested_start_date", models.DateField()),
                ("requested_end_date", models.DateField()),
                ("pending", models.BooleanField(default=True)),
                (
                    "owner_org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="download_owner",
                        to="staticdata.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="value_field",
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
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("field_name", models.CharField(max_length=100, unique=True)),
                (
                    "ladder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "owner_org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="value_field_owner",
                        to="staticdata.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="value_spec",
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
                ("name", models.CharField(max_length=30, unique=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "market_data_source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="value_spec_source",
                        to="classifiers.market_data_source",
                    ),
                ),
                (
                    "owner_org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="value_spec_owner",
                        to="staticdata.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="xrate_ladder",
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
                ("value_date", models.DateField()),
                (
                    "bid_xrate",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.0)]
                    ),
                ),
                (
                    "ask_xrate",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.0)]
                    ),
                ),
                (
                    "download",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="xrate_download",
                        to="marketdata.download",
                    ),
                ),
                (
                    "instrument",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="staticdata.instrument",
                    ),
                ),
                (
                    "owner_org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="xrate_owner",
                        to="staticdata.organization",
                    ),
                ),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="staticdata.identifier",
                    ),
                ),
                (
                    "value_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="xrate_value_field",
                        to="marketdata.value_field",
                    ),
                ),
                (
                    "value_spec",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="xrate_value_spec",
                        to="marketdata.value_spec",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="value_field_to_spec",
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
                    "value_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="value_field_to_spec_field",
                        to="marketdata.value_field",
                    ),
                ),
                (
                    "value_spec",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="value_field_to_spec_spec",
                        to="marketdata.value_spec",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="price_ladder",
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
                ("value_date", models.DateField()),
                (
                    "bid_price",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.0)]
                    ),
                ),
                (
                    "ask_price",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.0)]
                    ),
                ),
                (
                    "download",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="price_download",
                        to="marketdata.download",
                    ),
                ),
                (
                    "instrument",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="staticdata.instrument",
                    ),
                ),
                (
                    "owner_org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="price_owner",
                        to="staticdata.organization",
                    ),
                ),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="staticdata.identifier",
                    ),
                ),
                (
                    "value_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="price_value_field",
                        to="marketdata.value_field",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="download_tickers",
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
                    "download",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="marketdata.download",
                    ),
                ),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="staticdata.identifier",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="download_data",
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
                ("value_date", models.DateField()),
                (
                    "bid_price",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "ask_price",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "rate_value",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "download",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="data_download",
                        to="marketdata.download",
                    ),
                ),
                (
                    "instrument",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="staticdata.instrument",
                    ),
                ),
                (
                    "owner_org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="download_data_owner",
                        to="staticdata.organization",
                    ),
                ),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="staticdata.identifier",
                    ),
                ),
                (
                    "value_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="download_value_field",
                        to="marketdata.value_field",
                    ),
                ),
                (
                    "value_spec",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="download_value_spec",
                        to="marketdata.value_spec",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="download",
            name="value_spec",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="price_value_spec",
                to="marketdata.value_spec",
            ),
        ),
        migrations.CreateModel(
            name="analytics_ladder",
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
                ("value_date", models.DateField()),
                ("value", models.FloatField()),
                (
                    "download",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="analytics_download",
                        to="marketdata.download",
                    ),
                ),
                (
                    "instrument",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="staticdata.instrument",
                    ),
                ),
                (
                    "owner_org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="analytics_owner",
                        to="staticdata.organization",
                    ),
                ),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="staticdata.identifier",
                    ),
                ),
                (
                    "value_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="analytics_value_field",
                        to="marketdata.value_field",
                    ),
                ),
                (
                    "value_spec",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="analytics_value_spec",
                        to="marketdata.value_spec",
                    ),
                ),
            ],
        ),
    ]
