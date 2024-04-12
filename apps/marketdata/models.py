from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator



class value_field(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    field_name = models.CharField(max_length=100, unique=True)
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="value_field_owner")

class value_spec(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    market_data_source = models.ForeignKey("classifiers.market_data_source", on_delete=models.PROTECT, related_name="value_spec_source")
    ladder = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="value_spec_owner")

class value_field_to_spec(models.Model):
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="value_field_to_spec_field")
    value_spec = models.ForeignKey(value_spec, on_delete=models.PROTECT, related_name="value_field_to_spec_spec")

class download_data(models.Model):
    download_datetime = models.DateTimeField(blank=False, null=False, auto_now_add=True, unique=False)
    value_date = models.DateField(blank=False, null=False, unique=False)
    instrument = models.ForeignKey("staticdata.instrument", on_delete=models.CASCADE)
    bid_price = models.FloatField(null=True,blank=True,unique=False,validators=[MinValueValidator(0.0)],)
    ask_price = models.FloatField(null=True,blank=True,unique=False,validators=[MinValueValidator(0.0)],)
    rate_value = models.FloatField(null=True,blank=True,unique=False,validators=[MinValueValidator(0.0)],)
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="download_value_field")
    value_spec = models.ForeignKey(value_spec, on_delete=models.PROTECT, related_name="download_value_spec")
    ticker = models.ForeignKey("staticdata.identifier", on_delete=models.CASCADE)
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="download_data_owner")

class download(models.Model):
    download_data = models.ForeignKey(download_data, on_delete = models.DO_NOTHING, related_name = "download_data_link")

class price_ladder(models.Model):
    value_date = models.DateField(blank=False, null=False, unique=False)
    instrument = models.ForeignKey("staticdata.instrument", on_delete=models.CASCADE)
    bid_price = models.FloatField(null=False,blank=False,unique=False,validators=[MinValueValidator(0.0)],)
    ask_price = models.FloatField(null=False,blank=False,unique=False,validators=[MinValueValidator(0.0)],)
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="price_value_field")
    value_spec = models.ForeignKey(value_spec, on_delete=models.PROTECT, related_name="price_value_spec")
    ticker = models.ForeignKey("staticdata.identifier", on_delete=models.CASCADE)
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="price_owner")

class xrate_ladder(models.Model):
    value_date = models.DateField(blank=False, null=False, unique=False)
    instrument = models.ForeignKey("staticdata.instrument", on_delete=models.CASCADE)
    bid_xrate = models.FloatField(null=False,blank=False,unique=False,validators=[MinValueValidator(0.0)],)
    ask_xrate = models.FloatField(null=False,blank=False,unique=False,validators=[MinValueValidator(0.0)],)
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="xrate_value_field")
    value_spec = models.ForeignKey(value_spec, on_delete=models.PROTECT, related_name="xrate_value_spec")
    ticker = models.ForeignKey("staticdata.identifier", on_delete=models.CASCADE)
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="xrate_owner")

class analytics_ladder(models.Model):
    value_date = models.DateField(blank=False, null=False, unique=False)
    instrument = models.ForeignKey("staticdata.instrument", on_delete=models.CASCADE)
    value = models.FloatField(null=False,blank=False,unique=False)
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="analytics_value_field")
    value_spec = models.ForeignKey(value_spec, on_delete=models.PROTECT, related_name="analytics_value_spec")
    ticker = models.ForeignKey("staticdata.identifier", on_delete=models.CASCADE)
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="analytics_owner")