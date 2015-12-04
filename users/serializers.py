# -*- coding: utf-8 -*-
# __author__ = 'gloria'

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from users.models import Profile

class StringToFloatField(serializers.Field):

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return float(data)



class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    latitude = StringToFloatField()
    longitude = StringToFloatField()

    class Meta:
        model=Profile
        fields = ('id','user','avatar', 'latitude','longitude','city','state','sales')
        depth =1

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user.set_password(user.password)
        profile=Profile.objects.create(user=user, **validated_data)
        return profile


class ProfileUpdateSerializer(ProfileSerializer):

    user = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta(ProfileSerializer.Meta):
        fields=('user','avatar','latitude','longitude','city','state','sales')

class ProfileListSerializer(ProfileSerializer):
    class Meta (ProfileSerializer.Meta):
        fields=('user','avatar','latitude','longitude','city','state','sales')
        depth = 1
