from .models import Carrier, Transportable, Matching
from rest_framework import serializers

class TransportableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transportable
        fields = ['id','position','receiver','sender']

class CarrierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Carrier
        fields = ['id','position','phone','driver','plate_number']

class MatchingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Matching
        fields = []
