from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stops/', stops.as_view(), name='stop'),
    path('stopdetail/<str:stopid>', stopdetail.as_view(), name='stopdetail'),
    path('stopbylatlong/<str:plat>/<str:plong>', stopByLatLong.as_view(), name='StopBylatlong'),
    path('bus/<str:pk>', Bus.as_view(), name='bus'),
    path('busSchedule/<str:pk>', BusSchedule.as_view(), name='buschedule'),
    
]
