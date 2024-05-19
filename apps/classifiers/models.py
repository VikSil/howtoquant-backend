from django.db import models
from django.utils.timezone import now


class identifier_type(models.Model):
    type_name = models.CharField(max_length=25, unique=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)


class organization_type(models.Model):
    type_name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)

class instrument_class(models.Model):
    instrument_type = models.CharField(max_length=25)
    instrument_class = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)

class currency(models.Model):
    major_unit = models.CharField(max_length=50)
    minor_unit = models.CharField(max_length=30)
    major_to_minor = models.SmallIntegerField()
    ISO = models.CharField(max_length = 3, unique = True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)

class country(models.Model):
    name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=40)
    ISO2 = models.CharField(max_length=2, unique=True)
    ISO3 = models.CharField(max_length=3, unique=True)
    ccy = models.ForeignKey(currency, on_delete=models.PROTECT)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)

class industry_sector(models.Model):
    sector_name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)

class industry_subsector(models.Model):
    subsector_name = models.CharField(max_length=255, unique=True)
    sector = models.ForeignKey(industry_sector, on_delete = models.CASCADE)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)

class market_data_source(models.Model):
    source_name = models.CharField(max_length=100, unique=True)
    function_name = models.CharField(max_length=100, unique=False, blank=True, null=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)


class accounting_method(models.Model):
    method_name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=255, blank= True, null = True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)


class trade_status(models.Model):
    code = models.CharField(max_length=1, unique=True)
    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)


class position_type(models.Model):
    type_name = models.CharField(max_length=60, unique=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)


class accrual_type(models.Model):
    type_name = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)


class asset_flow_type(models.Model):
    type_name = models.CharField(max_length=60, unique=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)
