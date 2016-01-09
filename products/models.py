#-*- coding: utf-8 -*-

from django.db import models

from users.models import Profile

from .settings import PRODUCT_NAME_MAX_LENGTH, CATEGORY_NAME_MAX_LENGTH, QUERY_MAX_LENGTH


class Category(models.Model):

    # Ponemos el plural bien, si no saldría Categorys
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=CATEGORY_NAME_MAX_LENGTH)
    index = models.PositiveIntegerField(unique=True)

    def __unicode__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=PRODUCT_NAME_MAX_LENGTH)
    description = models.TextField(blank=True, null=True, default="")
    published_date = models.DateTimeField(auto_now_add=True)
    selling = models.BooleanField(default=True)
    price = models.FloatField()
    seller = models.ForeignKey(Profile)
    # al eliminar la categoría lo ponemos a null
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

# TODO: Actualizar el número de productos vendidos del seller cuando cambie selling

class SavedSearch(models.Model):

    query = models.CharField(max_length=QUERY_MAX_LENGTH)
    user = models.ForeignKey(Profile)
    # al eliminar la categoría lo ponemos a null
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.query

# TODO: Decidir si vamos a pasar a minúsculas y quitar los caracteres especiales en el pre-save

class Transaction(models.Model):

    product = models.ForeignKey(Product)
    buyer = models.ForeignKey(Profile, related_name='buyer')
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.product.name + u': ' + u' -> ' + self.buyer.user.username

# TODO: Controlar que product.seller y buyer NO son iguales
