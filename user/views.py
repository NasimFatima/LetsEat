import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json

from .models import User
from .serializer import UserSerializer
from .services.loginService import LoginService

# from django.views.decorators.debug import sensitive_post_parameters

# Create your views here.


@permission_classes([AllowAny])
class CustomRegisterView(RegisterView):
    """
    CustomRegisterView class for django-rest-auth
    that extends RegisterView. Create function is
    overriden to return a more detailed response
    """

    def create(self, request, *args, **kwargs):

        try:
            if User.objects.filter(email=request.data['email']).exists():
                return Response({"error": "User Email already exists!"}, status.HTTP_400_BAD_REQUEST)
            user = UserSerializer(data=request.data)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response = {
                "status": 200,
                "resp": self.get_response_data(user)
            }
            return Response(response,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        except Exception as err:
            return Response({"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([AllowAny])
class LoginView(LoginService):

    def post(self, request, *args, **kwargs):
        """

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        self.user = self.serializer.validated_data['user']
        self.login()
        response = self.get_response()
        return response


@permission_classes([AllowAny])
class GoogleView(LoginService):
    def post(self, request):
        payload = {'access_token': request.data.get(
            "token")}  # validate the token
        r = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {
                'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.email = data['email']
            # provider random default password
            user.password = make_password(
                BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()
        self.user = user
        self.login()
        response = self.get_response()
        return response
