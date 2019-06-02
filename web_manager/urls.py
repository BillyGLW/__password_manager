"""password_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

from .views import *

app_name = "web_manager"

urlpatterns = [
    path('', index, name="index"),
    path('login/', login_user, name="login_user"),
    path('logout/', wm_logout, name="wm_logout"),
    url(r'^profile/(?P<username>[\w.@+-]+)/delete/', wm_delete, name="wm_delete"),
    url(r'^profile/(?P<username>[\w.@+-]+)/update/$', wm_update, name="wm_update"),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', manage_password, name="manage_password"),
    url(r'^profile/(?P<username>[\w.@+-]+)/save/$', wm_password_update, name="wm_password_update"),
    url(r'^profile/(?P<username>[\w.@+-]+)/share/$', shared_link, name="shared_link"),
    url(r'^profile/(?P<username>[\w.@+-]+)/get_hash/(?P<hash>[\w.@+-]+)/(?P<enc>[-\w/\\=+/\s]+)/$', shared_link_update, name="shared_link_update"),
    url(r'^profile/(?P<username>[\w.@+-]+)/get_hash/$', wm_shared_link_generate, name="wm_shared_link_generate"),
    url(r'^profile/(?P<username>[\w.@+-]+)/get_hash/is_valid$', wm_shared_password_handle, name="wm_shared_password_handle"),

]
