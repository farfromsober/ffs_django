# -*- coding: utf-8 -*-
import math

class LocalizationManager:

    earth_radius = 6371

    @classmethod
    def calculate_point(cls, source_point, bearing, distance):
        '''
        :param source_point: tupla donde el primer elemento es la latitud y el segundo la longitud de un punto
        :param bearing: número de grados que queremos girar para obtener el nuevo punto
        :param distance: distancia que nos queremos desplazar
        :return: tupla con el punto resultante
        '''

        lat = math.radians(source_point[0])
        lon = math.radians(source_point[1])
        brng = math.radians(bearing)
        d = math.radians(distance)
        R = math.radians(cls.earth_radius)

        lat2 = math.asin(math.sin(lat) * math.cos(d/R) + math.cos(lat) * math.sin(d/R) * math.cos(brng))
        lon2 = lon + math.atan2(math.sin(brng) * math.sin(d/R) * math.cos(lat),
                                math.cos(d/R) - math.sin(lat) * math.sin(lat2))

        return math.degrees(lat2), math.degrees(lon2)


    @classmethod
    def calculate_distance(cls, point_a, point_b):
        """
        :param point_a:
        :param point_b:
        :return: devuelve la distancia en km desde el punto A al punto B
        """
        lat_a = math.radians(point_a[0])
        lon_a = math.radians(point_a[1])
        lat_b = math.radians(point_b[0])
        lon_b = math.radians(point_b[1])

        x = (lon_b - lon_a) * math.cos((lat_a + lat_b) / 2)
        y = (lat_b - lat_a)

        return math.sqrt(x*x + y*y) * cls.earth_radius