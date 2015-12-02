# -*- coding: utf-8 -*-
from .permissions import ProductPermission
from products.settings import DEFAULT_CATEGORY_INDEX
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from users.models import Profile
from .serializers import ProductSerializer, ProductCreationSerializer, ProductListSerializer
from .models import Product, Category
from rest_framework.response import Response


class ProductViewSet(GenericViewSet):

    # pagination_class = PageNumberPagination
    serializer_class = ProductSerializer
    permission_classes = (ProductPermission,)

    def list(self, request):
        products = self.get_products_queryset(request)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductCreationSerializer(data=request.data)
        if serializer.is_valid():
            category = get_object_or_404(Category, index=request.data.get('category', dict())
                                                                     .get('index', DEFAULT_CATEGORY_INDEX))
            product = serializer.save(seller=request.user.profile, category=category)
            response_serializer = ProductListSerializer(product)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
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

    def get_products_queryset(self, request):
        # gestion del filtro por categorias
        category_index = request.query_params.get('category', None)
        if category_index is not None:
            category = get_object_or_404(Category, index=category_index)
            products = Product.objects.prefetch_related('images').filter(category=category).order_by('-published_date', 'id')
        else:
            products = Product.objects.prefetch_related('images').order_by('-published_date', 'id')
        return products

    def get_categories_queryset(self, request):
        categories = Category.objects.order_by('index')
        return categories