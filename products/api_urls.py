# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import ProductViewSet, TransactionViewSet, BoughtAPIView

# APIRouter
router = DefaultRouter()
router.register(r'products', ProductViewSet, base_name='products_list_api')
router.register(r'transactions', TransactionViewSet, base_name='transactions_list_api')

urlpatterns = [
    # API URLs
    url(r'1.0/', include(router.urls)),  # incluyo las URLS de API
    url(r'1.0/products-bought/', BoughtAPIView.as_view())

]
