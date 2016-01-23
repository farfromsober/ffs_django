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
    city = models.CharField(max_length=CITY_MAX_LENGTH, null=True, blank=True)
    state = models.CharField(max_length=STATE_MAX_LENGTH, null=True, blank=True)
    sales = models.PositiveIntegerField(default=0)

    # propiedades calculadas
    full_name = property(lambda Profile: u'%s %s' % (Profile.user.first_name, Profile.user.last_name))

    def __unicode__(self):
        return u'[' + str(self.id) + u'] ' + self.user.username

# TODO: Añadirle una latitud y longitud si no nos viene dada
