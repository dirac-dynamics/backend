from .models import Carrier, Transportable
from rest_framework import serializers

class TransportableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transportable
        fields = ['id','position','position','sender']

class CarrierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Carrier
        fields = ['id','position','phone','driver','plate_number']
