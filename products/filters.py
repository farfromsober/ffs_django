# -*- coding: utf-8 -*-
import django_filters
from .models import Product, Transaction


class ProductsFilter(django_filters.FilterSet):

    category = django_filters.NumberFilter(name="category__index")

    class Meta:
        model = Product
        fields = ('category',)

class TransactionsFilter(django_filters.FilterSet):

    sellerId = django_filters.NumberFilter(name="product__seller__id")

    class Meta:
        model = Transaction
        fields = ('sellerId',)
