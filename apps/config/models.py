from django.db import models
from django.utils.timezone import now

class msg_queue(models.Model):
    source = models.CharField(max_length=50)
    source_id = models.BigIntegerField()
    destination = models.CharField(max_length=50)
    process = models.CharField(max_length=50)
    routine = models.CharField(max_length=100, blank=True, null=True)
    arg1 = models.CharField(max_length=100, blank=True, null=True)
    arg2 = models.CharField(max_length=100, blank=True, null=True)
    arg3 = models.CharField(max_length=100, blank=True, null=True)
    arg4 = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)
