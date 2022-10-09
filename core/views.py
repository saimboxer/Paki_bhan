from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import LocationSerializer
from .models import *

# Create your views here.
class stops(APIView):

    def get(self, request, *args, **kwargs):
        locations =  Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

class stopById(APIView):

    def get(self, request, pk, **kwargs):
        locations =  Location.objects.get(id=pk)
        serializer = LocationSerializer(locations, many=False)
        return Response(serializer.data)

class stopByLatLong(APIView):

    def get(self, request, plat, plong, **kwargs):
        locations =  Location.objects.get(lat=plat , long=plong)
        serializer = LocationSerializer(locations, many=False)
        return Response(serializer.data)              
