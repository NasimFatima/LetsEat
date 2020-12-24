import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from ..models import User
from ..serializer.user_serializer import UserSerializer
from ..services.loginService import LoginService

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
                return Response({"error": "User Email already exists!", "Success": False}, status.HTTP_200_OK)
            role = request.data['role']
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = self.perform_create(serializer)
                user.groups.add(role)
                headers = self.get_success_headers(serializer.data)
                user_data = UserSerializer(user).data
                response = {
                    'token': self.token,
                    'Success': True,
                    "status": 200,
                    'user': user_data
                }
                return Response(response,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
            else:
                return Response({"error": serializer.errors, "Success": False}, status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response({"error": "err"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([AllowAny])
class LoginView(LoginService):

    def post(self, request, *args, **kwargs):

        try:
            print("request.data", request.data)
            self.request = request
            self.serializer = self.get_serializer(data=self.request.data,
                                                  context={'request': request})
            self.serializer.is_valid(raise_exception=True)
            self.user = self.serializer.validated_data['user']
            self.login()
            response = self.get_response()
        except Exception as err:
            print("login", err)
            return Response({"error": "Unable to Login with Provided Credentials", "Success": False})
        return response


@ permission_classes([AllowAny])
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
            user, created = User.objects.get_or_create(email=data['email'])
            if created:
                user.password = make_password(
                    BaseUserManager().make_random_password())
                user.email = data['email']
                user.save()

            self.user = user
            self.login()
            response = self.get_response()
            return response
        except Exception as err:
            return Response({"error": "Unable to Login with Provided Credentials", "Success": False})
