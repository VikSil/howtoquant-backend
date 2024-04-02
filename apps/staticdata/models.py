from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class organization(models.Model):
    org_type_id = models.ForeignKey("classifiers.organization_type", on_delete=models.PROTECT)
    short_name = models.CharField(max_length=25)
    long_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    owner_org_id = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)


class instrument(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=35)
    instrument_class_id = models.ForeignKey("classifiers.instrument_class", on_delete=models.PROTECT)
    domicile_id = models.ForeignKey("classifiers.country", on_delete=models.PROTECT)
    base_ccy_id = models.ForeignKey("classifiers.currency", on_delete=models.PROTECT)
    issuer_id = models.ForeignKey(organization, on_delete=models.PROTECT, related_name = "instrument_issuer")
    owner_org_id = models.ForeignKey(organization, on_delete=models.PROTECT, related_name="instrument_owner")


class identifier(models.Model):
    code = models.CharField(max_length=25, unique=True)
    identifier_type_id = models.ForeignKey("classifiers.identifier_type", on_delete=models.PROTECT)
    instrument_id = models.ForeignKey(instrument, on_delete=models.CASCADE)
    owner_org_id = models.ForeignKey(organization, on_delete=models.PROTECT)


class equity(models.Model):
    instrument_id = models.ForeignKey(instrument, on_delete=models.CASCADE)
    dividend_frequency = models.SmallIntegerField(default = 4)
    sector_id = models.ForeignKey("classifiers.industry_sector", on_delete=models.PROTECT, default =999)
    subsector_id = models.ForeignKey("classifiers.industry_subsector", on_delete=models.PROTECT, default=999)
