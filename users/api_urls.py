# -*- coding: utf-8 -*-
# __author__ = 'gloria'

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from users.api import UserViewSet
from users.api import LoginAPIView


# APIRouter
router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')


urlpatterns = [
    # API URLs
    url(r'1.0/', include(router.urls)),  # incluyo las URLS de API
    url(r'1.0/login/$', LoginAPIView.as_view()),
]