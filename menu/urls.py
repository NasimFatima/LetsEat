from django.conf.urls import include, url
from django.urls import re_path

from .views import (MenuViewSet, MenuItemViewSet)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'menuItems', MenuViewSet, 'menu')
router.register(r'Items', MenuItemViewSet, 'items')

urlpatterns = router.urls
