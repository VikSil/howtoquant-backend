from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator


class value_field(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    field_name = models.CharField(max_length=100, unique=True)
    market_data_source = models.ForeignKey(
        "classifiers.market_data_source", on_delete=models.PROTECT, related_name="value_field_source"
    )

class value_spec(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)    
    ladder = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="value_spec_owner")

class value_field_to_spec(models.Model):
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="value_field_to_spec_field")
    value_spec = models.ForeignKey(value_spec, on_delete=models.PROTECT, related_name="value_field_to_spec_spec")

class download(models.Model):
    start_datetime = models.DateTimeField(blank=False, null=False, auto_now_add=True, unique=False)
    complete_datetime = models.DateTimeField(blank=True, null=True, unique=False)
    requested_start_date = models.DateField(blank=False, null=False, unique=False)
    requested_end_date = models.DateField(blank=False, null=False, unique=False)
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="download_owner")
    pending = models.BooleanField(blank=False, null=False, default=True)

class download_tickers(models.Model):
    download = models.ForeignKey(download, on_delete=models.CASCADE)
    ticker = models.ForeignKey("staticdata.identifier", on_delete=models.CASCADE)

class download_data(models.Model):
    download = models.ForeignKey(download, on_delete=models.DO_NOTHING, related_name = "data_download")
    value_date = models.DateField(blank=False, null=False, unique=False)
    instrument = models.ForeignKey("staticdata.instrument", on_delete=models.CASCADE)
    bid_price = models.FloatField(null=True,blank=True,unique=False,validators=[MinValueValidator(0.0)],)
    ask_price = models.FloatField(null=True,blank=True,unique=False,validators=[MinValueValidator(0.0)],)
    rate_value = models.FloatField(null=True,blank=True,unique=False,validators=[MinValueValidator(0.0)],)
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="download_value_field")
    ticker = models.ForeignKey("staticdata.identifier", on_delete=models.CASCADE)


class price_ladder(models.Model):
    value_date = models.DateField(blank=False, null=False, unique=False)
    instrument = models.ForeignKey("staticdata.instrument", on_delete=models.CASCADE)
    bid_price = models.FloatField(null=False,blank=False,unique=False,validators=[MinValueValidator(0.0)],)
    ask_price = models.FloatField(null=False,blank=False,unique=False,validators=[MinValueValidator(0.0)],)
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="price_value_field")
    ticker = models.ForeignKey("staticdata.identifier", on_delete=models.CASCADE)
    download = models.ForeignKey(download, on_delete=models.DO_NOTHING, related_name = "price_download")
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="price_owner")

class xrate_ladder(models.Model):
    value_date = models.DateField(blank=False, null=False, unique=False)
    instrument = models.ForeignKey("staticdata.instrument", on_delete=models.CASCADE)
    bid_xrate = models.FloatField(null=False,blank=False,unique=False,validators=[MinValueValidator(0.0)],)
    ask_xrate = models.FloatField(null=False,blank=False,unique=False,validators=[MinValueValidator(0.0)],)
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="xrate_value_field")
    ticker = models.ForeignKey("staticdata.identifier", on_delete=models.CASCADE)
    download = models.ForeignKey(download, on_delete=models.DO_NOTHING, related_name="xrate_download")
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="xrate_owner")

class analytics_ladder(models.Model):
    value_date = models.DateField(blank=False, null=False, unique=False)
    instrument = models.ForeignKey("staticdata.instrument", on_delete=models.CASCADE)
    value = models.FloatField(null=False,blank=False,unique=False)
    value_field = models.ForeignKey(value_field, on_delete=models.PROTECT, related_name="analytics_value_field")
    ticker = models.ForeignKey("staticdata.identifier", on_delete=models.CASCADE)
    download = models.ForeignKey(download, on_delete=models.DO_NOTHING, related_name="analytics_download")
    owner_org = models.ForeignKey("staticdata.organization", on_delete=models.PROTECT, related_name="analytics_owner")
