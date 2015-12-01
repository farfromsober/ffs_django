# -*- coding: utf-8 -*-
from .models import Product, Category
from rest_framework.generics import get_object_or_404


class ProductsQueryset(object):

    def get_products_queryset(self, request):
        # gestion del filtro por categorias
        category_index = request.query_params.get('category', None)
        if category_index is not None:
            category = get_object_or_404(Category, index=category_index)
            products = Product.objects.filter(category=category).order_by('-published_date', 'id')
        else:
            products = Product.objects.order_by('-published_date', 'id')
        return products

    def get_categories_queryset(self, request):
        categories = Category.objects.order_by('index')
        return categories
