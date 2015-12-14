# -*- coding: utf-8 -*-
#__author__ = 'dregatos'
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from images.serializers import ImageSerializer, ImageCreateSerializer
from products.serializers import ProductListSerializer
from products.models import Product
from .models import Image
from django.shortcuts import get_object_or_404


class ImageViewSet(GenericViewSet):

    queryset = Image.objects.all()
    serializer_class = ImageSerializer  # default one
    #permission_classes = (ImagePermission,)

    def create(self, request):
        #TODO comprobar que el product pertenece al request.user
        serializer = ImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            # recuperamos el producto
            product = get_object_or_404(Product, pk=request.data.get('productId'))
            # creamos el objeto image
            serializer.save(product=product, url=request.data.get('url'))
            # devolvemos el producto completo
            response_serializer = ProductListSerializer(product)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def update(self, request, pk):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def destroy(self, request, pk):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
