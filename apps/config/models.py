from django.db import models
from django.utils.timezone import now


class msg_queue(models.Model):
    '''
    Model/Table contains all messages to be processed or being processed by backend services

    Possible flags:
    N - New - Will be picked up for processing by the designated service
    F - Flow processing - msg sent to FlowBooker
    P - Position processing - msg sent to PositionManager
    X - Terminated - work on the message complete
    Y - Downstream failure - error occured during downstream processing
    Z - Failure - error occured during processing by the designated service
    '''

    source = models.CharField(max_length=50)
    source_id = models.BigIntegerField()
    destination = models.CharField(max_length=50)
    process = models.CharField(max_length=50)
    routine = models.CharField(max_length=100, blank=True, null=True)
    flag = models.CharField(max_length=1)
    arg1 = models.CharField(max_length=100, blank=True, null=True)
    arg2 = models.CharField(max_length=100, blank=True, null=True)
    arg3 = models.CharField(max_length=100, blank=True, null=True)
    arg4 = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(default=now, blank=True, unique=False)
    updated = models.DateTimeField(default=now, blank=True, unique=False)
