# -*- coding: utf-8 -*-
#__author__ = 'dregatos'
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from images.permissions import ImagePermission
from images.serializers import ImageCreateSerializer, ImageDestroySerializer
from products.models import Product
from products.serializers import ProductListSerializer
from .models import Image


class ImageViewSet(GenericViewSet):

    queryset = Image.objects.all()
    permission_classes = (ImagePermission,)

    # sobreescribimos este método para especificar distintos serializers
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ImageDestroySerializer
        elif self.request.method == 'POST':
            return ImageCreateSerializer

    def create(self, request):
        serializer = ImageCreateSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        # compruebo si el usuario autenticado puede hacer GET en este product
        self.check_object_permissions(request, product)
        serializer = ProductListSerializer(product)
        return Response(data=serializer.get_images(product),status=status.HTTP_200_OK)

    def update(self, request, pk):
        serializer = ImageDestroySerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            url = request.data.get('url')
            image = Image.objects.get(url=url)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)