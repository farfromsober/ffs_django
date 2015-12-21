# -*- coding: utf-8 -*-
import django_filters

from .localization import calculate_point
from .models import Product
from users.models import Profile


class ProductsFilter(django_filters.FilterSet):

    category = django_filters.NumberFilter(name="category__index")
    name = django_filters.CharFilter(name='name', lookup_type='icontains')
    seller = django_filters.CharFilter(name='seller__user__username')
    selling = django_filters.BooleanFilter(name='selling')

    class Meta:
        model = Product
        fields = ('category', 'name', 'seller', 'selling')





def filter_with_localization(params, products):
    """
    :param params: get parameters de la request
    :return: si tenemos los parámetros necesarios para el filtrado por localización devolvemos los productos que entren
     dentro del cuadrado formado con el punto de origen y la distancia dada
    """
    lat = params.get('latitude', None)
    lon = params.get('longitude', None)
    dist = params.get('distance', None)
    if lat and lon and dist:

        try:
            source_point = (float(lat), float(lon))
            distance = float(dist)
        except:
            return products

        north_point = calculate_point(source_point, 0, distance)
        west_point = calculate_point(source_point, 90, distance)
        south_point = calculate_point(source_point, 180, distance)
        east_point = calculate_point(source_point, 270, distance)

        profiles = Profile.objects.filter(latitude__lte=north_point[0], latitude__gte=south_point[0],
                                          longitude__lte=west_point[1], longitude__gte=east_point[1])

        return products.filter(seller__in=profiles)


    return products