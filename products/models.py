#-*- coding: utf-8 -*-

from django.db import models

from users.models import Profile

from .settings import PRODUCT_NAME_MAX_LENGTH, CATEGORY_NAME_MAX_LENGTH, QUERY_MAX_LENGTH




class Category(models.Model):
    name = models.CharField(max_length=CATEGORY_NAME_MAX_LENGTH)
    index = models.PositiveIntegerField(unique=True)





class Product(models.Model):

    name = models.CharField(max_length=PRODUCT_NAME_MAX_LENGTH)
    description = models.TextField(blank=True, null=True, default="")
    published_date = models.DateTimeField(auto_now_add=True)
    selling = models.BooleanField(default=True)
    price = models.FloatField()
    seller = models.ForeignKey(Profile)
    # al eliminar la categoría lo ponemos a null
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

# TODO: Pre-save para actualizar el número de productos vendidos del seller cuando cambie selling




class SavedSearch(models.Model):

    query = models.CharField(max_length=QUERY_MAX_LENGTH)
    user = models.ForeignKey(Profile)
    # al eliminar la categoría lo ponemos a null
    category = models(Category, null=True, on_delete=models.SET_NULL)

# TODO: Decidir si vamos a pasar a minúsculas y quitar los caracteres especiales en el pre-save






class Transaction(models.Model):

    product = models.ForeignKey(Product)
    seller = models.ForeignKey(Profile)
    buyer = models.ForeignKey(Profile)
    date = models.DateTimeField(auto_now_add=True)


