from pyexpat import model
from django.db import models

# Create your models here.
class role(models.Model):
    role = models.CharField(max_length=50)
    role_short_name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.role

class app_user(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.IntegerField()
    role = models.ForeignKey(role, on_delete=models.CASCADE)
    is_active = models.BooleanField()
    is_password_exp = models.BooleanField()
    last_login = models.DateTimeField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.first_name        

class user(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.username    

class vhicle(models.Model):
    reg_number = models.CharField(max_length=100)
    vhcl_type = models.CharField(max_length=5)
    seating_capacity = models.IntegerField()
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField()
    updated_by = models.CharField(max_length=100)

    def __str__(self):	
        return self.reg_number       

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

class location(models.Model):
    location_name = models.CharField(max_length=100)
    location_short_name = models.CharField(max_length=20)
    city_id = models.ForeignKey(city, on_delete=models.CASCADE)
    loc_type = models.CharField(max_length=20)
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
    route_name = models.CharField(max_length=100) 
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
