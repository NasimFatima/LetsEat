from datetime import datetime

from rest_auth.serializers import (LoginSerializer)
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings as jwt_settings
from ..serializer import UserSerializer


def login(self):
    self.token = jwt_encode(self.user)
    serializer = UserSerializer(instance=self.user,
                                context={'request': self.request})
    data = {
        'token': self.token,
        'Success': True,
        'user': serializer.data
    }
    response = Response(
        data, status=status.HTTP_200_OK)
    return response
