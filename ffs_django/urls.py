"""ffs_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from users import api_urls as users_api_urls
from products import api_urls as products_api_urls
from images import api_urls as images_api_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),



    #Users API URLs
    url(r'api/', include(users_api_urls)),

    # Products URLs
    url(r'api/', include(products_api_urls)),

    # Images URLs
    url(r'api/', include(images_api_urls)),
]
