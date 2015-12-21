# -*- coding: utf-8 -*-
import django_filters
from .models import Product


class ProductsFilter(django_filters.FilterSet):

    category = django_filters.NumberFilter(name="category__index")
    name = django_filters.CharFilter(name='name', lookup_type='icontains')
    seller = django_filters.CharFilter(name='seller__user__username')

    class Meta:
        model = Product
        fields = ('category', 'name', 'seller')
