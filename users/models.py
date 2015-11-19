#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from .settings import CITY_MAX_LENGTH, STATE_MAX_LENGTH

# En Django no es buena idea la herencia de modelos, por este motivo
# creamos la clase Profile y asociamos el usuario con una clave foránea
class Profile(models.Model):

    user = models.OneToOneField(User)

    avatar = models.URLField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=CITY_MAX_LENGTH)
    state = models.CharField(max_length=STATE_MAX_LENGTH)
    sales = models.PositiveIntegerField(default=0)

# TODO: Pre-save para añadirle una latitud y longitud si no nos viene dada
