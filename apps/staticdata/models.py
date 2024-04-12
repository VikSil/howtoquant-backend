from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class organization(models.Model):
    org_type = models.ForeignKey("classifiers.organization_type", on_delete=models.PROTECT)
    short_name = models.CharField(max_length=25)
    long_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    owner_org = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)


class instrument(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=35)
    instrument_class = models.ForeignKey("classifiers.instrument_class", on_delete=models.PROTECT)
    domicile = models.ForeignKey("classifiers.country", on_delete=models.PROTECT)
    base_ccy = models.ForeignKey("classifiers.currency", on_delete=models.PROTECT)
    issuer = models.ForeignKey(organization, on_delete=models.PROTECT, related_name = "instrument_issuer")
    owner_org = models.ForeignKey(organization, on_delete=models.PROTECT, related_name="instrument_owner")


class identifier(models.Model):
    code = models.CharField(max_length=25, unique=True)
    identifier_type = models.ForeignKey("classifiers.identifier_type", on_delete=models.PROTECT)
    instrument = models.ForeignKey(instrument, on_delete=models.CASCADE)
    owner_org = models.ForeignKey(organization, on_delete=models.PROTECT)


class equity(models.Model):
    instrument = models.ForeignKey(instrument, on_delete=models.CASCADE)
    dividend_frequency = models.SmallIntegerField(default = 4)
    sector = models.ForeignKey("classifiers.industry_sector", on_delete=models.PROTECT, default =999)
    subsector = models.ForeignKey("classifiers.industry_subsector", on_delete=models.PROTECT, default=999)
