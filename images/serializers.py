# -*- coding: utf-8 -*-
#__author__ = 'dregatos'

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from models import Image
from products.serializers import ProductSerializer


class StringToFloatField(serializers.Field):

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return float(data)


class ImageSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    #urls = 'handle' url array

    class Meta:
        model = Image


class ImageCreateSerializer(ImageSerializer):

    product = PrimaryKeyRelatedField(read_only='False')

    class Meta:
        model = Image
