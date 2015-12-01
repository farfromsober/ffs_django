# -*- coding: utf-8 -*-
from .settings import DEFAULT_CATEGORY_INDEX
from rest_framework import serializers
from models import Product, Category
from rest_framework.relations import PrimaryKeyRelatedField
from users.serializers import ProfileSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'index')


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    seller = ProfileSerializer()

    # TODO: enviar array de imagenes de un producto

    class Meta:
        model = Product


class ProductListSerializer(ProductSerializer):

    price = serializers.SerializerMethodField('price_string')
    id = serializers.SerializerMethodField('id_string')

    def price_string(self, obj):
        return '{0}'.format(obj.price)

    def id_string(self, obj):
        return '{0}'.format(obj.id)

    class Meta:
        model = Product


class ProductCreationSerializer(ProductSerializer):

    category = PrimaryKeyRelatedField(read_only='False')

    # class Meta(ProductSerializer.Meta):
    #     fields = ('id', 'name', 'description', 'price', 'category',)

    @staticmethod
    def category_index(data):
        if isinstance(data, dict):
            index_received = data.get('index')
            if not index_received == None:
                index = index_received
            else:
                 index = DEFAULT_CATEGORY_INDEX
        else:
            index = DEFAULT_CATEGORY_INDEX
        return index
