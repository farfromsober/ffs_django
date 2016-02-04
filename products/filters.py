# -*- coding: utf-8 -*-
import django_filters

from .localization import LocalizationManager
from .models import Product, Transaction
from users.models import Profile

class TransactionsFilter(django_filters.FilterSet):

    sellerId = django_filters.NumberFilter(name="product__seller__id")

    class Meta:
        model = Transaction
        fields = ('sellerId',)




class ProductsFilter(django_filters.FilterSet):

    category = django_filters.NumberFilter(name="category__index")
    name = django_filters.CharFilter(name='name', lookup_type='icontains')
    seller = django_filters.CharFilter(name='seller__user__username')
    selling = django_filters.BooleanFilter(name='selling')

    class Meta:
        model = Product
        fields = ('category', 'name', 'seller', 'selling')





def get_point_and_distance(params):
    """
    :param params: get parameters de la request
    :return: si tenemos los parámetros necesarios, devolvemos el punto y la distancia pasados en los params
    """
    lat = params.get('latitude', None)
    lon = params.get('longitude', None)
    dist = params.get('distance', None)

    if lat and lon and dist:

        try:
            source_point = (float(lat), float(lon))
            distance = float(dist)
            return source_point, distance
        except:
            return None, None

    return None, None




def filter_with_localization(params, queryset):
    """
    :param params: get parameters de la request
    :return: si tenemos los parámetros necesarios para el filtrado por localización devolvemos los productos que entren
     dentro del cuadrado formado con el punto de origen y la distancia dada
    """
    source_point, distance = get_point_and_distance(params)

    if source_point and distance:

        north_point = LocalizationManager.calculate_point(source_point, 0, distance)
        west_point = LocalizationManager.calculate_point(source_point, 90, distance)
        south_point = LocalizationManager.calculate_point(source_point, 180, distance)
        east_point = LocalizationManager.calculate_point(source_point, 270, distance)

        profiles = Profile.objects.filter(latitude__lte=north_point[0], latitude__gte=south_point[0],
                                          longitude__lte=west_point[1], longitude__gte=east_point[1])

        return queryset.filter(seller__in=profiles)

    return queryset



def add_distance(params, products):
    """
    :param params: get parameters de la request
    :param data: json con los productos filtrados
    :return: añade un campo distancia al json de productos
    """

    source_point = get_point_and_distance(params)[0]

    if source_point:

        for product in products:
            seller = product['seller']
            destination_point = (float(seller['latitude']), float(seller['longitude']))
            product['distance'] = LocalizationManager.calculate_distance(source_point, destination_point)