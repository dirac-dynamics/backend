from .models import Carrier, Transportable
from rest_framework import serializers

class TransportableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transportable
        fields = ['position', 'destination']

class CarrierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Carrier
        fields = ['position']
