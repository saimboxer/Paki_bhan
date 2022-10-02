from django.contrib.auth.models import User
from django.db import models

from core.models import Location, Vehicle, VehicleClass


class Ticket(models.Model):
    pnr_no = models.CharField(max_length=20, unique = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dep_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='departure_tickets')
    arrival_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='arrival_tickets')
    traveller = models.CharField(max_length=100)
    journey_datetime = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    vehicle_class = models.ForeignKey(VehicleClass, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=True)
    seatreserved = models.CharField(max_length=20)
    offer_applied = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return self.pnr_no