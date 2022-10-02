from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Country)
admin.site.register(City)

admin.site.register(Vehicle)
admin.site.register(VehicleClass)
admin.site.register(Location)
admin.site.register(Platform)

