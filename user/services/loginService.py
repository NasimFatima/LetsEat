"""[summary]

Returns:
    [type]: [description]
"""
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_auth.serializers import TokenSerializer, JWTSerializer, LoginSerializer
from rest_framework.authtoken.models import Token as TokenModel
from rest_auth.utils import jwt_encode, default_create_token as create_token
from django.conf import settings
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings as jwt_settings
from datetime import datetime


class LoginService(GenericAPIView):
    """[summary]

    Args:
        GenericAPIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    serializer_class = LoginSerializer
    token_model = TokenModel

    def get_response_serializer(self):
        """[Format Response based on Setting]

        Returns:
            object: Formatted response
        """
        response_serializer = JWTSerializer
        return response_serializer

    def get_response(self):
        """get response based on token method

        Returns:
            [type]: [description]
        """
        serializer_class = self.get_response_serializer()
        data = {
            'user': self.user,
            'token': self.token
        }
        serializer = serializer_class(instance=data,
                                      context={'request': self.request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
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
                                      self.serializer)
