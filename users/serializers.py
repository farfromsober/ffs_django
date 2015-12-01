# -*- coding: utf-8 -*-
# __author__ = 'gloria'
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Profile


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model=Profile
        fields = ('user','avatar', 'latitude','longitude','city','state','sales')
        depth =1

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user.set_password(user.password)
        profile=Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):

        user_data=validated_data.pop('user')
        user = instance.user

        user.first_name = user_data.get('first_name')
        user.last_name = user_data.get('last_name')
        user.email = user_data.get('email')
        user.set_password(user_data.get('password'))
        user.save()

        instance.avatar = validated_data.get('avatar')
        instance.latitude = validated_data.get('latitude')
        instance.longitude = validated_data.get('longitude')
        instance.city = validated_data.get('city')
        instance.state = validated_data.get('state')
        instance.sales = validated_data.get('sales')
        instance.save()

        return instance



class ProfileListSerializer(ProfileSerializer):
    class Meta (ProfileSerializer.Meta):
        fields=('user','avatar','latitude','longitude','city','state','sales')
        depth = 1
