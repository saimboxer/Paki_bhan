from email.policy import default
from enum import unique
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
# class role(models.Model):
#     role = models.CharField(max_length=50)
#     role_short_name = models.CharField(max_length=50)
#     created_at = models.DateTimeField()
#     created_by = models.CharField(max_length=100)
#     updated_at = models.DateTimeField()
#     updated_by = models.CharField(max_length=100)

#     def __str__(self):	
#         return self.role

class country(models.Model):
    cnt_name = models.CharField(max_length=100)
    cnt_short_name = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.cnt_name

class city(models.Model):
    city_name = models.CharField(max_length=100)
    city_short_name = models.CharField(max_length=20)
    cnt_id = models.ForeignKey(country, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.city_name

class app_user(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.IntegerField()
    age = models.IntegerField()
    address = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    city = models.ForeignKey(city, on_delete=models.CASCADE)
    cnt = models.ForeignKey(country, on_delete=models.CASCADE)
#    role = models.ForeignKey(role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default = True)
    is_password_exp = models.BooleanField(default = False)
    last_login = models.DateTimeField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.first_name        

# class user(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     dob = models.DateField()
#     email = models.EmailField()
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     is_active = models.BooleanField()
#     created_at = models.DateTimeField()
#     created_by = models.CharField(max_length=100)
#     updated_at = models.DateTimeField()
#     updated_by = models.CharField(max_length=100)

#     def __str__(self):	
#         return self.username    

class vhicle(models.Model):
    reg_number = models.CharField(max_length=100)
    vhcl_type = models.CharField(max_length=5) # vihicle type = Bus, Tram, Train 
    vhcl_capacity = models.IntegerField()
    is_cyclespace_available = models.BooleanField(default = True)
    is_toilet_available = models.BooleanField(default = True)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.reg_number       

class vhicle_class(models.Model):
    vhcl_id = models.ForeignKey(vhicle, on_delete=models.CASCADE)
    class_type = models.CharField(max_length=20) # General, sleeper, 1AC, 2AC, 3AC 
    capacity = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.vhcl_id 

class location(models.Model):
    loc_name = models.CharField(max_length=100)
    loc_short_name = models.CharField(max_length=20)
    city_id = models.ForeignKey(city, on_delete=models.CASCADE)
    loc_type = models.CharField(max_length=20) # location type = Bus/Tram stop, Train station 
    long = models.FloatField()
    lat = models.FloatField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.location_name         

class plateform(models.Model):
    plateform_name = models.CharField(max_length=10)
    loc_id = models.ForeignKey(location, on_delete=models.CASCADE)
    long = models.FloatField()
    lat = models.FloatField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.plateform_name

class route(models.Model):
    route_name = models.CharField(max_length=50) 
    route_id = models.CharField(max_length=20) #from_Loc_sn - to_Loc_sn
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.route_name

class route_dtl(models.Model):
    route_id = models.ForeignKey(route, on_delete=models.CASCADE)
    loc_id = models.ForeignKey(location, on_delete=models.CASCADE)
    order = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.route_id  
        
class vhicle_schedule(models.Model):
    vhcl_id = models.ForeignKey(vhicle, on_delete=models.CASCADE)
    route_id = models.ForeignKey(route, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    est_start_time = models.TimeField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.vhcl_id

class ticket(models.Model):
    pnr_no = models.CharField(max_length=20, unique = True)
    user_id = models.ForeignKey(app_user, on_delete=models.CASCADE)
    dep_loc_id = models.ForeignKey(location, on_delete=models.CASCADE)
    arrival_loc_id = models.ForeignKey(location, on_delete=models.CASCADE)
    traveller = models.CharField(max_length=100)
    journey_datetime = models.DateTimeField()
    vhcl_id = models.ForeignKey(vhicle, on_delete=models.CASCADE)
    rserved_class = models.ForeignKey(vhicle_class, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default = True)
    seatreserved = models.CharField(max_length=20)
    offer_applied = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.pnr_no

class payment(models.Model):
    trnx_no = models.IntegerField()
    tkt_id = models.ForeignKey(ticket, on_delete=models.CASCADE)
    bank  = models.CharField(max_length=100)
    card_no = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.trnx_no        