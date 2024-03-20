from rest_framework import serializers
from .models import *

class identifier_type_serializer (serializers.ModelSerializer):
    class Meta:
        model = identifier_type
        fields = ['id', 'type_name']
        