from django.conf.urls import include, url
from django.urls import re_path
from rest_auth.registration.views import VerifyEmailView

from .view.user import (CustomRegisterView, GoogleView, LoginView)
from .view.user_groups import GroupViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'group', GroupViewSet, 'group')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'registration/', CustomRegisterView.as_view(),
        name='my_custom_registration'),
    url(r'login/', LoginView.as_view(), name='my_login_view'),
    url(r'google/', GoogleView.as_view(), name='google')
]
