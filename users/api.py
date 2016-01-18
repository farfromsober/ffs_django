# -*- coding: utf-8 -*-
from users.models import Profile

__author__ = 'gloria'

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.permissions import UserPermission
from users.serializers import ProfileSerializer, ProfileUpdateSerializer, ProfileListSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

from django.contrib.auth import login, authenticate
from rest_framework.views import APIView


class UserViewSet(GenericViewSet):

    serializer_class = ProfileSerializer
    # pagination_class = PageNumberPagination
    permission_classes = (UserPermission,)
    queryset = Profile.objects.all()

    def list(self, request):
        users = Profile.objects.all()
        serializer = ProfileListSerializer(users, many=True)
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
        profile = get_object_or_404(Profile, pk=pk)
        #Verificar  si el usuario puede actualizar
        self.check_object_permissions(request, profile)
        serializer = ProfileUpdateSerializer(instance=profile, data=request.data)
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


class LoginAPIView(APIView):

   def post(self, request, format=None):

       username = request.data.get("user", None)
       password = request.data.get("password", None)

       if username is not None and password is not None:

           user = authenticate(username=username, password=password)

           if user is not None and user.is_active:

               login(request, user)
               profile = get_object_or_404(Profile, user=user)
               serializer = ProfileSerializer(profile)
               return Response(serializer.data, status=status.HTTP_200_OK)

           else:

               return Response(status=status.HTTP_401_UNAUTHORIZED)

       else:

           return Response(status=status.HTTP_400_BAD_REQUEST)

