from django.db import models

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
    instrument = models.PositiveIntegerField
    instrument_class = models.ForeignKey(instrument_class, on_delete=models.CASCADE)
