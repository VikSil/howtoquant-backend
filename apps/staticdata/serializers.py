from rest_framework import serializers
from .models import *

class IdentifierTypeSerializer (serializers.ModelSerializer):
    class Meta:
        model = identifier_type
        fields = ['id', 'type_name']
        