# -*- coding: utf-8 -*-
#__author__ = 'dregatos'

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import ImageViewSet

# APIRouter
router = DefaultRouter()
router.register(r'images', ImageViewSet, base_name='image_list')

urlpatterns = [
    # API URLs
    url(r'1.0/', include(router.urls)),  # incluyo las URLS de API
]