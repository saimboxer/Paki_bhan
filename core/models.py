from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    """
        `ISO 3166 Country Codes <https://www.iso.org/iso-3166-country-codes.html>`_
        The field names are a bit awkward, but kept for backwards compatibility.
        pycountry's syntax of alpha2, alpha3, name and official_name seems sane.
        """
    iso_3166_1_a2 = models.CharField(
        _('ISO 3166-1 alpha-2'), max_length=2, primary_key=True)
    iso_3166_1_a3 = models.CharField(
        _('ISO 3166-1 alpha-3'), max_length=3, blank=True)
    iso_3166_1_numeric = models.CharField(
        _('ISO 3166-1 numeric'), blank=True, max_length=3)

    #: The commonly used name; e.g. 'United Kingdom'
    printable_name = models.CharField(_('Country name'), max_length=128, db_index=True)
    #: The full official name of a country
    #: e.g. 'United Kingdom of Great Britain and Northern Ireland'
    name = models.CharField(_('Official name'), max_length=128)

    display_order = models.PositiveSmallIntegerField(
        _("Display order"), default=0, db_index=True,
        help_text=_('Higher the number, higher the country in the list.'))

    is_shipping_country = models.BooleanField(
        _("Is shipping country"), default=False, db_index=True)

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    def __str__(self):
        return self.printable_name or self.name

    @property
    def code(self):
        """
        Shorthand for the ISO 3166 Alpha-2 code
        """
        return self.iso_3166_1_a2

    @property
    def numeric_code(self):
        """
        Shorthand for the ISO 3166 numeric code.
        :py:attr:`.iso_3166_1_numeric` used to wrongly be a integer field, but has to
        be padded with leading zeroes. It's since been converted to a char
        field, but the database might still contain non-padded strings. That's
        why the padding is kept.
        """
        return "%.03d" % int(self.iso_3166_1_numeric)


class City(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_created_city", blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_updated_city", blank=True, null=True
    )

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")

    def __str__(self):	
        return self.name


class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = (("Bus" , "Bus"),
                        ("Train" , "Train"),
                        ("Tram" , "Tram"))

    reg_number = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=5, choices = VEHICLE_TYPE_CHOICES, default = 'Bus' )
    vhcl_capacity = models.IntegerField()
    is_cyclespace_available = models.BooleanField(default = True)
    is_toilet_available = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_created_vehicle", blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_updated_vehicle", blank=True, null=True
    )

    def __str__(self):	
        return self.reg_number       


class VehicleClass(models.Model):
    CLASS_TYPE_CHOICES = (("GEN" , "General"),
                        ("SLPR" , "Sleeper"),
                        ("1AC" , "1AC"),
                        ("2AC" , "2AC"),
                        ("3AC" , "3AC"))

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    class_type = models.CharField(max_length=5, choices = CLASS_TYPE_CHOICES)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_created_vehicleclass", blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_updated_vehicleclass", blank=True, null=True
    )  
    def __str__(self):	
        return self.vehicle

    class Meta:
        verbose_name = _("vehicle class")
        verbose_name_plural = _("vehicle classes")

class Location(models.Model):
    LOCATION_TYPE_CHOICES = (("STOP" , "Stop"),
                        ("STATION" , "Train Station"))

    name = models.CharField(max_length=100)
    loc_short_name = models.CharField(max_length=20, blank = True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    loc_type = models.CharField(max_length=10, choices = LOCATION_TYPE_CHOICES)
    lat = models.FloatField()
    long = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_created_location", blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_updated_location", blank=True, null=True
    )

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=10)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    long = models.FloatField()
    lat = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_created_platform", blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_updated_platform", blank=True, null=True
    )

    def __str__(self):	
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=30) 
    code = models.CharField(max_length=20) #from_Loc_sn - to_Loc_sn
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_created_route", blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_updated_route", blank=True, null=True
    )

    def __str__(self):	
        return self.name


class RouteDetail(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    order = models.IntegerField()
    arrive_in_min = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_created_routedetail", blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_updated_routedetail", blank=True, null=True
    )

    def __str__(self):	
        return self.route.name

    class Meta:
        unique_together = (('route', 'location'),)  


class VehicleSchedule(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    est_start_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_created_vehicleschedule", blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_updated_vehicleschedule", blank=True, null=True
    )

    def __str__(self):	
        return self.route.name
