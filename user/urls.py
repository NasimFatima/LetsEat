from django.conf.urls import include, url
from django.urls import re_path
from rest_auth.registration.views import VerifyEmailView

from .view.user import (CustomRegisterView, GoogleView, LoginView,
                        get_user_dummy_method)
from .view.user_groups import get_all_roles

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'registration/', CustomRegisterView.as_view(),
        name='my_custom_registration'),
    url(r'login/', LoginView.as_view(), name='my_login_view'),
    url(r'google/', GoogleView.as_view(), name='google'),
    url(r'dummy/', get_user_dummy_method, name='get user dummy method'),
    url(r'getroles/', get_all_roles, name='get all roles'),
]
