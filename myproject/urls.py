from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    url(r'^', include('messenger.urls')),
    url(r'^admin/', admin.site.urls),
   	
]