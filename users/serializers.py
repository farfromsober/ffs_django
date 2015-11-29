# -*- coding: utf-8 -*-
# __author__ = 'gloria'
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Profile


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('id')

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('username','password')


    def validate(self, data):
        print('********')
        self.user = authenticate(username=data.get('username'), password=data.get('password'))
        print('********')
        print(data.get('username'))
        print('********')
        print(self.user)
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError('inactive_account')
            return data
        else:
            raise serializers.ValidationError('invalid_credentials')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model=Profile
        fields = ('user','avatar', 'latitude','longitude','city','state','sales')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        profile=Profile.objects.create(user=user, **validated_data)
        return profile






class ProfileListSerializer(ProfileSerializer):
    class Meta (ProfileSerializer.Meta):
        fields=('user','avatar','latitude','longitude','city','state','sales')
        depth = 1
