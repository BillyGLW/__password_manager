from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

from .views import *
from web_manager.views import *

from .apps import PasswordManagerConfig

# app_name = PasswordManagerConfig.name

urlpatterns = [
	# url('', include('web_manager.urls')),
    url(r'^page=etc/passwd/$', rrol, name="rrol"),
    path('admin/', admin.site.urls),
    path('web_manager/', include('web_manager.urls')),
    path('v1/', include('v1.urls')),
]
