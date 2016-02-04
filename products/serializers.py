# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import Product, Category, Transaction
from rest_framework.relations import PrimaryKeyRelatedField
from users.serializers import ProfileSerializer
from users.models import Profile


class StringToFloatField(serializers.Field):

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return float(data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'index')


##################################
        ## PRODUCT ##
##################################


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    seller = ProfileSerializer()
    price = StringToFloatField()
    id = StringToFloatField()
    images = serializers.SerializerMethodField()  # utiliza el metodo "get_images"

    class Meta:
        model = Product

    def get_images(self, obj):
        return obj.images.all().values_list('url', flat=True)


class ProductCreateSerializer(ProductSerializer):

    category = PrimaryKeyRelatedField(read_only='False')

    class Meta(ProductSerializer.Meta):
        fields = ('name', 'description', 'price', 'category')


class ProductUpdateSerializer(ProductSerializer):

    category = PrimaryKeyRelatedField(read_only='False')

    class Meta(ProductSerializer.Meta):
        fields = ('name', 'description', 'price', 'category', 'selling')



##################################
        ## TRANSACTION ##
##################################

class TransactionSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    buyer = ProfileSerializer()

    class Meta:
        model = Transaction


class TransactionListSerializer(TransactionSerializer):

    class Meta:
        model = Transaction

class TransactionCreateSerializer(serializers.Serializer):

    productId = serializers.IntegerField()
    buyerId = serializers.IntegerField()

    def validate_productId(self, value):
        """
        Check:
               1. format
               2. a product exists with this id
        """
        try:
            int(value)
        except:
            raise serializers.ValidationError("Invalid format on productId")

        product = Product.objects.get(pk=value)
        if product is None:
            raise serializers.ValidationError("Invalid productId")

        return value

    def validate_buyerId(self, value):
        """
        Check:
                1. format
                2. a user exists with this id
        """
        try:
            int(value)
        except:
            raise serializers.ValidationError("Invalid format on buyerId")

        buyer = Profile.objects.get(pk=value)
        if buyer is None:
            raise serializers.ValidationError("Invalid buyerId")

        return value


