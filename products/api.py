# -*- coding: utf-8 -*-
from .permissions import ProductPermission
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from users.models import Profile
from .views import ProductsQueryset
from .serializers import ProductSerializer, ProductCreationSerializer, ProductListSerializer
from .models import Product, Category
from rest_framework.response import Response


class ProductViewSet(ProductsQueryset, GenericViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (ProductPermission,)

    def list(self, request):
        products = self.get_products_queryset(request)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductCreationSerializer(data=request.data)
        if serializer.is_valid():
            # 'category' selection with static method to get the index
            category = get_object_or_404(Category, index=ProductCreationSerializer.category_index(request.data.get('category')))
            # 'seller' from the request user
            seller = get_object_or_404(Profile, user=request.user)
            serializer.save(seller=seller, category=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)  # compruebo si el usuario autenticado puede hacer GET en este product
        serializer = ProductListSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)  # compruebo si el usuario autenticado puede hacer PUT en este product
        serializer = ProductCreationSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            seller = get_object_or_404(Profile, user=request.user)
            serializer.save(seller=seller)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)  # compruebo si el usuario autenticado puede hacer DELETE en este product
        if product.selling:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
