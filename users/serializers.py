# -*- coding: utf-8 -*-
# __author__ = 'gloria'
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Profile
from users.settings import STATE_MAX_LENGTH, CITY_MAX_LENGTH


class StringToFloatField(serializers.Field):

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return float(data)



class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name','email')

class UserListSerializer (UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('id','username','first_name', 'last_name','email')



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





class ProfileListSerializer(ProfileSerializer):
    user = UserListSerializer()
    class Meta (ProfileSerializer.Meta):
        fields=('user','avatar','latitude','longitude','city','state','sales')







class UserUpdateSerializer(serializers.Serializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(allow_blank=True, allow_null=True)
    password = serializers.CharField(required=False)

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)






class ProfileUpdateSerializer(serializers.Serializer):

    avatar = serializers.URLField(allow_null=True, allow_blank=True)
    latitude = serializers.CharField(max_length=50)
    longitude = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=CITY_MAX_LENGTH, allow_null=True, allow_blank=True)
    state = serializers.CharField(max_length=STATE_MAX_LENGTH, allow_null=True, allow_blank=True)
    sales = serializers.IntegerField(min_value=0)
    user = UserUpdateSerializer()


    def update(self, instance, validated_data):

        instance.avatar = validated_data.get('avatar', instance.avatar)

        # latitud y longitud hay que pasarlos a float
        instance.latitude = float(validated_data.get('latitude', instance.latitude))
        instance.longitude = float(validated_data.get('longitude', instance.longitude))

        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.sales = validated_data.get('sales', instance.sales)

        # actualizamos el usuario
        user_dict = validated_data.get('user', None)
        if user_dict is not None:
            instance.user.first_name = user_dict.get('first_name', instance.user.first_name)
            instance.user.last_name = user_dict.get('last_name', instance.user.last_name)
            instance.user.email = user_dict.get('email', instance.user.email)

            # solo actualizamos el password en caso de que nos venga
            new_password = user_dict.get('password', None)
            if new_password is not None:
                instance.user.password = make_password(new_password)

        instance.save()
        instance.user.save()
        return instance


    def validate_sales(self, value):
        if value < 0:
            raise serializers.ValidationError(u'Las ventas no pueden ser menores que cero')
        return value



    def validate_latitude(self, value):
        try:
            float(value)
        except:
            raise serializers.ValidationError(u'El formato de la latitud introducida no es válido')
        return value


    def validate_longitude(self, value):
        try:
            float(value)
        except:
            raise serializers.ValidationError(u'El formato de la longitud introducida no es válido')
        return value









