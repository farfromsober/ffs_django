# -*- coding: utf-8 -*-
#__author__ = 'dregatos'

from rest_framework import serializers

from models import Image
from products.models import Product

class ImageCreateSerializer(serializers.Serializer):

    productId = serializers.IntegerField()
    urls = serializers.ListField(
        child=serializers.URLField()
    )

    def validate_productId(self, value):
        """
        Check:
               1. format
               2. a product exists with this id
               3. that product belongs to request.user
        """
        try:
            int(value)
        except:
            raise serializers.ValidationError("Invalid format on productId")

        product = Product.objects.get(pk=value)
        if product is None:
            raise serializers.ValidationError("Invalid productId")

        user = self.context.get('user')
        if product.seller.user != user:
            raise serializers.ValidationError("You don't have permission to modify that product")

        return value

    def create(self, validated_data):
        product = Product.objects.get(pk=validated_data.get('productId'))
        for url in validated_data.get('urls'):
            Image.objects.create(product=product, url=url)
        return product

class ImageDestroySerializer(serializers.Serializer):

    url = serializers.URLField()

    def validate_url(self, value):
        """
        Check:
               1. image exists
               2. that image belongs to request.user
        """
        image = Image.objects.get(url=value)
        if image is None:
          raise serializers.ValidationError("Unknown url")

        user = self.context.get('user')
        if image.product.seller.user != user:
            raise serializers.ValidationError("You don't have permission to modify that product")

        return value


