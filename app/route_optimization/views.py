from .models import Carrier, Transportable
from .serializers import CarrierSerializer, TransportableSerializer
from rest_framework import viewsets
from rest_framework import permissions


class CarrierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Carrier.objects.all().order_by('-id')
    serializer_class = CarrierSerializer
    permission_classes = [permissions.AllowAny]

class TransportableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transportable.objects.all().order_by('-id')
    serializer_class = TransportableSerializer
    permission_classes = [permissions.AllowAny]