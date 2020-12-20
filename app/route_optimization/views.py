from .models import Carrier, Transportable, Matching
from .serializers import CarrierSerializer, TransportableSerializer, MatchingSerializer
from rest_framework import views, viewsets
from rest_framework import permissions


class CarrierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Carrier.objects.all().order_by('id')
    serializer_class = CarrierSerializer
    permission_classes = [permissions.AllowAny]

class TransportableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transportable.objects.all().order_by('id')
    serializer_class = TransportableSerializer
    permission_classes = [permissions.AllowAny]

class MatcherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that triggers the matching.
    """
    queryset =  Matching.objects.all()
    serializer_class = MatchingSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        # optimization goes here
        return {}
