from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, time, timedelta

from .serializer import *
from .models import *

# Create your views here.
class stops(APIView):

    def get(self, request, *args, **kwargs):
        locations =  Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

class stopByLatLong(APIView):

    def get(self, request, plat, plong, **kwargs):
        locations =  Location.objects.get(lat=plat , long=plong)
        serializer = LocationSerializer(locations, many=False)
        return Response(serializer.data)

class Bus(APIView):

    def get(self, request, pk, *args, **kwargs):
        Bus =  Vehicle.objects.get(id=pk)
        serializer = BusSerializer(Bus, many=False)
        return Response(serializer.data)            

class BusSchedule(APIView):

    def get(self, request, pk, *args, **kwargs):
        BusSchedule =  VehicleSchedule.objects.get(id=pk)
        serializer = BusScheduleSerializer(BusSchedule, many=False)
        serializer_data = serializer.data
        start_time = serializer_data.get("est_start_time")
        date_format_str = '%H:%M:%S'
        
        start_time = datetime.strptime(start_time,date_format_str)
        

        stops = serializer_data.get("stops")
        for stop in stops:
            arrive_at = start_time + timedelta(minutes=int(stop.get("arrive_in_min")))
            arrive_at = datetime.strftime(arrive_at,date_format_str)
            stop["arrive_at"] = arrive_at

        return Response(serializer.data)

    ## stop detail Api##
class stopdetail(APIView):

    def get(self, request, stopid, **kwargs):
        stoplist =  Location.objects.get(id=stopid)
        serializer = StopDetailSerializer(stoplist, many=False, context={"pstopid": stopid})        
        return Response(serializer.data)
