from django.contrib.auth.models import User, Group
from rest_framework import serializers

from web_manager.models import web_manager_password

import sys
sys.path.append("..") # Adds higher directory to python modules path.



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = web_manager_password
        fields = ['account_name', 'account_password', 'site_url', 'site_name']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class User_Password_Serializer(serializers.ModelSerializer):
	class Meta:
		model = web_manager_password
		fields = ['id', 'account_name', 'account_password']

class Create_User_Password_Serializer(serializers.ModelSerializer):
	class Meta:
		model = web_manager_password
		fields = ['id', 'account_password']
		