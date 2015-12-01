# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import ProductViewSet

# APIRouter
router = DefaultRouter()
router.register(r'products', ProductViewSet, 'products_list_api')

urlpatterns = [
    # API URLs
    url(r'1.0/', include(router.urls)),  # incluyo las URLS de API
]
