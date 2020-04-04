from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer, User_Password_Serializer, Create_User_Password_Serializer
from .pagination import CustomPagination
# from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticated, IsOwnerOrReadOnly

from web_manager.models import web_manager_password

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
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


class RWeb_get_delete_update_ManagerView(RetrieveUpdateDestroyAPIView):
    serializer_class = User_Password_Serializer
    pagination_class = CustomPagination
    # permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self, pk):
        try:
            web_manager = web_manager_password.objects.get(pk=pk)
        except web_manager_password.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return web_manager

    def get(self, request, pk):
        web_manager = self.get_queryset(pk)
        serializer = User_Password_Serializer(web_manager, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            content = {
                'status': 'Not Found',
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        web_manager = self.get_queryset(pk)

        if (str(request.user) == web_manager.account_name):
            serializer = Create_User_Password_Serializer(web_manager, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {
                'status': 'Not Authorized'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        web_manager = self.get_queryset(pk)

        if (str(request.user) == web_manager.account_name):
            web_manager.delete()
            content = {
                'status': 'Content Deleted'
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {
                'status' :'Not Authorized',
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


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
