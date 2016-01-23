#-*- coding: utf-8 -*-

from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):

    # columnas que se muestran en el listado
    list_display = ['__unicode__', 'full_name', 'sales']

    # para filtrar en la derecha
    #list_filter = ['user__username', 'full_name']

    # buscador
    #search_fields = ['user__username', 'full_name']


# Register your models here.
admin.site.register(Profile, ProfileAdmin)