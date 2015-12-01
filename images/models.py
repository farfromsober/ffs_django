#-*- coding: utf-8 -*-

from django.db import models

from products.models import Product



class Image(models.Model):

    product = models.ForeignKey(Product)
    url = models.URLField()

    def __unicode__(self):
        return self.product.name + u' - ' + self.url