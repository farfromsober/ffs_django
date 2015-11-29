# -*- coding: utf-8 -*-
from users.models import Profile

__author__ = 'gloria'
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.permissions import UserPermission
from users.serializers import ProfileSerializer, LoginSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

from django.contrib.auth import login
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class UserViewSet(GenericViewSet):

    serializer_class = ProfileSerializer
    # pagination_class = PageNumberPagination
    # permission_classes = (UserPermission,)
    queryset = Profile.objects.all()

    def list(self, request):
        users = Profile.objects.all()
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        user = get_object_or_404(Profile, pk=pk)

        #Se verifican permisos
        self.check_object_permissions(request, user)

        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        user = get_object_or_404(Profile, pk=pk)

        #Verificar  si el usuario puede actualizar
        self.check_object_permissions(request, user)
        serializer = ProfileSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user = get_object_or_404(Profile, pk=pk)

        #Verificar si el usuario puede borrar
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FFSBasicAuthentication(BasicAuthentication):

    def authenticate(self, request):
        user, _ = super(FFSBasicAuthentication, self).authenticate(request)
        login(request, user)
        return user


class LoginAPIView(APIView):

    serializer_class = LoginSerializer


    def post(self, request, format=None):

        serializer =LoginSerializer(data=request.data)

        if serializer.is_valid():
            content = {
                'user': unicode(request.user),
                'auth': unicode(request.auth),  # None
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
