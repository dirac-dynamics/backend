from .models import Carrier, Transportable, Matching
from .serializers import CarrierSerializer, TransportableSerializer, MatchingSerializer
from rest_framework import views, viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .graph import create_from_city



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

        print(carrier_positions)
        print(transportable_positions)

        # optimization goes here
        carrier_to_transportable_optimal, routes_optimal, carrier_to_transportable_greedy, routes_greedy  = create_from_city('Munich_2', 48.143743 + 0.05, 48.143743 - 0.05, 11.575942 + 0.10, 11.575942 - 0.10, len(carriers), len(transportables), random=False,carrier_list=carrier_positions, transportable_list=transportable_positions)

        return Response({'carrier_to_transport_optimal':carrier_to_transportable_optimal,
                         'routes_optimal':routes_optimal,
                         'carrier_to_transport_greedy':carrier_to_transportable_greedy,
                         'routes_greedy':routes_greedy})
