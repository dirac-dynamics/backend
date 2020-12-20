from .models import Carrier, Transportable, Matching
from .serializers import CarrierSerializer, TransportableSerializer, MatchingSerializer
from rest_framework import views, viewsets
from rest_framework import permissions
from rest_framework.response import Response


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
    def create(self, request, *args, **kwargs):
        carriers = Carrier.objects.all().order_by('id')
        transportables = Transportable.objects.all().order_by('id')

        carrier_positions = [c.position.coords for c in carriers]
        transportable_positions = [t.position.coords for t in transportables]

        # optimization goes here

        return Response({'yes':'no'})
