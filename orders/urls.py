from django.conf.urls import include, url
from .views import OrdersViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'orders', OrdersViewSet, 'group')

urlpatterns = router.urls
