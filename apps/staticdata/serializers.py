from rest_framework import serializers
from ..classifiers.models import identifier_type

class IdentifierTypeSerializer (serializers.ModelSerializer):
    class Meta:
        model = identifier_type
        fields = '__all__'

# POST serializer should be separate from GET serializer and fields can be specified
class CreateIdentifierTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = identifier_type
        fields = ['type_name'] 
