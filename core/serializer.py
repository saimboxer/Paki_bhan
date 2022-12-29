from rest_framework import serializers
from .models import *
from datetime import datetime

now = datetime.now()  # current date and time


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location model
    """

    class Meta:
        model = Location
        fields = "__all__"


class RoutDetailSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source="location.name")
    loc_type = serializers.ChoiceField(
        source="location.loc_type", choices=Location.LOCATION_TYPE_CHOICES
    )
    lat = serializers.FloatField(source="location.lat")
    long = serializers.FloatField(source="location.long")

    # start_time = serializers.TimeField(source='route.VehicleSchedule.est_start_time')

    class Meta:
        model = RouteDetail
        fields = ("location_name", "arrive_in_min", "loc_type", "lat", "long")


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            "id",
            "reg_number",
            "vehicle_type",
            "is_cyclespace_available",
            "is_toilet_available",
        )


class BusScheduleSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.CharField(source="vehicle.id")
    vehicle_reg_number = serializers.CharField(source="vehicle.reg_number")
    vehicle_type = serializers.CharField(source="vehicle.vehicle_type")
    is_cyclespace_available = serializers.CharField(
        source="vehicle.is_cyclespace_available"
    )
    is_toilet_available = serializers.CharField(source="vehicle.is_toilet_available")

    route = serializers.CharField(source="route.name")

    departure_info = serializers.SerializerMethodField("get_depart_info")
    arrival_info = serializers.SerializerMethodField("get_arrival_info")

    stops = serializers.SerializerMethodField("get_stop_list")

    def get_depart_info(self, obj):
        departure_stop = RouteDetail.objects.filter(route=obj.route).first()
        departure_stop = RoutDetailSerializer(departure_stop)
        return departure_stop.data

    def get_arrival_info(self, obj):
        arrival_stop = RouteDetail.objects.filter(route=obj.route).last()
        arrival_stop = RoutDetailSerializer(arrival_stop)
        return arrival_stop.data

    def get_stop_list(self, obj):
        stop_list = RouteDetail.objects.filter(route=obj.route).order_by("order")
        stop_list = RoutDetailSerializer(stop_list, many=True)
        return stop_list.data

    class Meta:
        model = VehicleSchedule
        fields = (
            "id",
            "route",
            "day",
            "est_start_time",
            "vehicle_id",
            "vehicle_reg_number",
            "vehicle_type",
            "is_cyclespace_available",
            "is_toilet_available",
            "departure_info",
            "arrival_info",
            "stops",
        )

    ## stop detail Api##


class RouteStopDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "name")


class StopRoutDetailSerializer(serializers.ModelSerializer):
    routename = serializers.CharField(source="route.name")
    last_stop = serializers.SerializerMethodField()
    today = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    # est_strt_time = serializers.SerializerMethodField()

    def get_time(self, obj):
        time_obj = now.strftime("%H:%M:%S")
        return time_obj

    def get_today(self, obj):
        today_obj = now.strftime("%A")
        return today_obj

    def get_last_stop(self, obj):
        last_route_obj = (
            RouteDetail.objects.filter(route__name=obj.route).order_by("-order").first()
        )
        return last_route_obj.location.name

    class Meta:
        model = RouteDetail
        fields = (
            "arrive_in_min",
            "routename",
            "route",
            "last_stop",
            "today",
            "time",
        )


class StopDetailSerializer(serializers.ModelSerializer):
    vehicle_schedule = serializers.SerializerMethodField("get_route_list")

    def get_route_list(self, obj):
        pstopid = self.context.get("pstopid")
        vnow = datetime.now()

        route_list = RouteDetail.objects.filter(location=pstopid)
        route_ids = [r.route.id for r in route_list]
        active_schedules = VehicleSchedule.objects.filter(
            day=vnow.strftime("%A"), est_start_time__gt=vnow, route_id__in=route_ids
        )
        active_route_ids = [r.route.id for r in active_schedules]
        final_list = route_list.filter(route_id__in=active_route_ids)
        route_list = StopRoutDetailSerializer(final_list, many=True)
        return route_list.data

    class Meta:
        model = Location
        fields = ("id", "name", "loc_type", "lat", "long", "vehicle_schedule")


class RouteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteDetail
        fields = "__all__"
