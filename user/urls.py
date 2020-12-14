from .views import CustomRegisterView, LoginView, GoogleView
from django.conf.urls import include, url
from django.urls import re_path
from rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'registration/', CustomRegisterView.as_view(),
        name='my_custom_registration'),
    url(r'login/', LoginView.as_view(), name='my_login_view'),
    url(r'google/', GoogleView.as_view(), name='google'),
]
