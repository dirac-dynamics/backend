import json
import os

from .models import Carrier, Transportable, Matching
from .serializers import CarrierSerializer, TransportableSerializer, MatchingSerializer
from rest_framework import views, viewsets
from dirac_django.settings import BASE_DIR
from rest_framework import permissions
from rest_framework.response import Response

from .solvers_hardcode import singlesolver_osmnx, greedy_singlesolver_osmnx
from .setup_data import carriers, targets, transportables, all_coord_routes, all_time, all_length, weight_list, connection_list_single, connection_number, weight_list_2, start_end_list

maps_path = os.path.join(BASE_DIR, 'maps')
import ast
import time

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
        #carriers = Carrier.objects.all().order_by('id')
        #transportables = Transportable.objects.all().order_by('id')

        #carrier_positions = [c.position.coords for c in carriers]
        #transportable_positions = [t.position.coords for t in transportables]


        routes, durations, distances = singlesolver_osmnx(carriers, targets, transportables, all_coord_routes, all_time, all_length, weight_list, connection_list_single, connection_number)

        time.sleep(2)

        return Response({'routes':routes,
                         'durations':durations,
                         'distances':distances})

class GreedyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that triggers the greedy matching.
    """
    queryset =  Matching.objects.all()
    serializer_class = MatchingSerializer
    permission_classes = [permissions.AllowAny]
    def create(self, request, *args, **kwargs):
        #carriers = Carrier.objects.all().order_by('id')
        #transportables = Transportable.objects.all().order_by('id')

        #carrier_positions = [c.position.coords for c in carriers]
        #transportable_positions = [t.position.coords for t in transportables]


        routes, durations, distances = greedy_singlesolver_osmnx(carriers, targets, transportables, all_coord_routes, all_time, all_length, weight_list_2, start_end_list)

        return Response({'routes':routes,
                         'durations':durations,
                         'distances':distances})
