from django.db import models

from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    """
        `iiISO 3166 Country Codes <https://www.iso.org/iso-3166-country-codes.html>`_
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
    city_name = models.CharField(max_length=100)
    city_short_name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")

    def __str__(self):	
        return self.city_name


class Vehicle(models.Model):
    reg_number = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=5) # vihicle type = Bus, Tram, Train
    vhcl_capacity = models.IntegerField()
    is_cyclespace_available = models.BooleanField(default = True)
    is_toilet_available = models.BooleanField(default = True)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.reg_number       


class VehicleClass(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    class_type = models.CharField(max_length=20) # General, sleeper, 1AC, 2AC, 3AC 
    capacity = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.vehicle

    class Meta:
        verbose_name = _("vehicle class")
        verbose_name_plural = _("vehicle classes")

class Location(models.Model):
    name = models.CharField(max_length=100)
    loc_short_name = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    loc_type = models.CharField(max_length=20) # location type = Bus/Tram stop, Train station 
    long = models.FloatField()
    lat = models.FloatField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=10)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    long = models.FloatField()
    lat = models.FloatField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.name


class Route(models.Model):
    route_name = models.CharField(max_length=50) 
    route = models.CharField(max_length=20) #from_Loc_sn - to_Loc_sn
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.route_name


class RouteDetail(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    order = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.route_id  


class VehicleSchedule(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    est_start_time = models.TimeField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.vehicle
