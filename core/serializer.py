from numpy import source
from rest_framework import serializers
from .models import *     

class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        fields = ('__all__')

class RoutDetailSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name')
    loc_type = serializers.ChoiceField(source='location.loc_type', choices=Location.LOCATION_TYPE_CHOICES)
    lat = serializers.FloatField(source='location.lat')
    long = serializers.FloatField(source='location.long')
    #start_time = serializers.TimeField(source='route.VehicleSchedule.est_start_time')

    class Meta:
        model = RouteDetail
        fields = ('location_name', 'arrive_in_min', 'loc_type', 'lat', 'long')               

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', 'reg_number', 'vehicle_type', 'is_cyclespace_available', 'is_toilet_available')


class BusScheduleSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.CharField(source='vehicle.id')
    vehicle_reg_number = serializers.CharField(source='vehicle.reg_number')
    vehicle_type = serializers.CharField(source='vehicle.vehicle_type')
    is_cyclespace_available = serializers.CharField(source='vehicle.is_cyclespace_available')
    is_toilet_available = serializers.CharField(source='vehicle.is_toilet_available')

    route = serializers.CharField(source='route.name')

    departure_info = serializers.SerializerMethodField('get_depart_info')
    arrival_info = serializers.SerializerMethodField('get_arrival_info')

    stops = serializers.SerializerMethodField('get_stop_list')

    def get_depart_info(self, obj):
            departure_stop = RouteDetail.objects.filter(route = obj.route).first()
            departure_stop = RoutDetailSerializer(departure_stop)
            return departure_stop.data

    def get_arrival_info(self, obj):
            arrival_stop = RouteDetail.objects.filter(route = obj.route).last()
            arrival_stop = RoutDetailSerializer(arrival_stop)
            return arrival_stop.data        

    def get_stop_list(self, obj):
            stop_list = RouteDetail.objects.filter(route = obj.route).order_by('order') 
            stop_list = RoutDetailSerializer(stop_list, many=True)
            return stop_list.data

    class Meta:
        model = VehicleSchedule
        fields = ('id', 'route', 'day', 'est_start_time', 'vehicle_id', 'vehicle_reg_number', 'vehicle_type', 
                  'is_cyclespace_available', 'is_toilet_available', 'departure_info', 'arrival_info', 'stops')



    ## stop detail Api##
class RouteStopDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('id','name')

class StopRoutDetailSerializer(serializers.ModelSerializer):
    routename = serializers.CharField(source='route.name')
    
    #last_stop = serializers.SerializerMethodField('get_arrival_info')

    print('#########################555555###########')
    print('#########################555555###########')
    print('#########################555555###########')
    print('#########################555555###########')
    print('#########################555555###########')
  #  print(route)

    #def get_arrival_info(self, obj):
    #        arrival_stop = RouteDetail.objects.filter(route = route).last()
    #        arrival_stop = RoutDetailSerializer(arrival_stop)
    #
    #        return arrival_stop.data  
    
    class Meta:
        model = RouteDetail
        fields = ('arrive_in_min', 'routename', 'route', )               


class StopDetailSerializer(serializers.ModelSerializer):
    
    vehicle_schedule = serializers.SerializerMethodField('get_route_list')
    def get_route_list(self, obj):
            pstopid = self.context.get("pstopid")
            route_list = RouteDetail.objects.filter(location=pstopid)
            route_list = StopRoutDetailSerializer(route_list, many=True)
            return route_list.data

    class Meta:
        model = Location
        fields = ('id','name','loc_type','lat','long','vehicle_schedule')

