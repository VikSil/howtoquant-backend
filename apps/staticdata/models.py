from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class instrument_class(models.Model):
    instrument_type = models.CharField(max_length = 25)
    instrument_class = models.CharField(max_length =50, unique = True)

class equity(models.Model):
    name = models.CharField(max_length=50, unique = True)
    instrument_class = models.ForeignKey(instrument_class, on_delete = models.PROTECT)


class identifier_type(models.Model):
    type_name = models.CharField(max_length=25, unique=True)


class identifier(models.Model):
    identifier = models.CharField(max_length=25, unique=True)
    identifier_type = models.ForeignKey(identifier_type, on_delete=models.PROTECT)
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="identifier")
    parent_id = models.PositiveIntegerField()
    parent = GenericForeignKey("parent_type", "parent_id")


