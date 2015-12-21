# -*- coding: utf-8 -*-
import math

def calculate_point(source_point, bearing, distance):
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
    R = math.radians(6371)

    lat2 = math.asin(math.sin(lat) * math.cos(d/R) + math.cos(lat) * math.sin(d/R) * math.cos(brng))
    lon2 = lon + math.atan2(math.sin(brng) * math.sin(d/R) * math.cos(lat),
                            math.cos(d/R) - math.sin(lat) * math.sin(lat2))

    return math.degrees(lat2), math.degrees(lon2)


