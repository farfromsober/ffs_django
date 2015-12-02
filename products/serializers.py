# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Product, Category
from rest_framework.relations import PrimaryKeyRelatedField
from users.serializers import ProfileSerializer


class StringToFloatField(serializers.Field):

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return float(data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'index')


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    seller = ProfileSerializer()
    price = StringToFloatField()
    id = StringToFloatField()
    images = serializers.SerializerMethodField()

    # TODO: enviar array de imagenes de un producto

    class Meta:
        model = Product

    def get_images(self, obj):
        return obj.image_set.all().values_list('url', flat=True)


class ProductListSerializer(ProductSerializer):

    class Meta:
        model = Product


class ProductCreationSerializer(ProductSerializer):

    category = PrimaryKeyRelatedField(read_only='False')

    class Meta(ProductSerializer.Meta):
        fields = ('name', 'description', 'price', 'category',)
