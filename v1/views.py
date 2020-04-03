from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer, User_Password_Serializer, Create_User_Password_Serializer
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated

from web_manager.models import web_manager_password

from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView

import sys
sys.path.append("..") # Adds higher directory to python modules path.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # permission_classes = (IsAuthenticated, )
    queryset = web_manager_password.objects.all().order_by('account_name')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class RWeb_ManagerView(ListCreateAPIView):
    serializer_class = User_Password_Serializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        web_manager = web_manager_password.objects.all()
        return web_manager

    def get(self, request):
        web_manager = self.get_queryset()
        paginate_queryset = self.paginate_queryset(web_manager)
        serializer = self.serializer_class(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        ''' C-reate View '''
        serializer = Create_User_Password_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(account_name=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_BAD_REQUEST)
