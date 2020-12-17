"""[summary]

Returns:
    [type]: [description]
"""
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import Group
from rest_auth.serializers import (JWTSerializer, LoginSerializer,
                                   TokenSerializer)
from rest_auth.utils import default_create_token as create_token
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.authtoken.models import Token as TokenModel
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings as jwt_settings

from ..serializer.user_serializer import UserSerializer


class LoginService(GenericAPIView):
    serializer_class = LoginSerializer
    token_model = TokenModel

    def get_response(self):
        serializer = UserSerializer(instance=self.user,
                                    context={'request': self.request})
        data = {
            'token': self.token,
            'Success': True,
            'user': serializer.data
        }
        response = Response(
            data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            if jwt_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)
        return response

    def login(self):
        """[summary]
        """
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      UserSerializer)
