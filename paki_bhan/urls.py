from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stops/', stops.as_view(), name='stop'),
    path('stopbyid/<str:pk>', stopById.as_view(), name='StopById'),
    path('stopbylatlong/<str:plat>/<str:plong>', stopByLatLong.as_view(), name='StopBylatlong'),
    
]
