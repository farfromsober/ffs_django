#-*- coding: utf-8 -*-

from django.contrib import admin
from .models import Product, Transaction, Category, SavedSearch


class ProductAdmin(admin.ModelAdmin):

    # columnas que se muestran en el listado
    list_display = ['name', 'published_date', 'seller', 'category', 'price', 'selling']

    # para filtrar en la derecha
    list_filter = ['category']

    # buscador
    search_fields = ['seller__user__username', 'name']




class SavedSearchAdmin(admin.ModelAdmin):

    # columnas que se muestran en el listado
    list_display = ['query', 'user', 'category']

    # para filtrar en la derecha
    list_filter = ['category']

    # buscador
    search_fields = ['user__user__username', 'query']





class TransactionAdmin(admin.ModelAdmin):

    # columnas que se muestran en el listado
    list_display = ['__unicode__', 'date']

    # buscador
    search_fields = ['product', 'seller__user__username', 'buyer__user__username']






# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
admin.site.register(SavedSearch, SavedSearchAdmin)
