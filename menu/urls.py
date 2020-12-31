from django.conf.urls import include, url
from django.urls import re_path

from .view.menu import (MenuViewSet, MenuItemViewSet)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'menuItems', MenuViewSet, 'menu')
router.register(r'Items', MenuItemViewSet, 'items')

urlpatterns = [
    url(r'^', include(router.urls))
]
