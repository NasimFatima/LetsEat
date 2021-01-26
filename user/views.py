import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_auth.registration.views import RegisterView
from rest_framework import status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from letseat.settings import MAX_EMPLOYEES
from .models import User
from .serializer import UserSerializer
from django.contrib.auth.models import Group
from .serializer import GroupSerializer
from rest_framework.generics import GenericAPIView
from rest_auth.serializers import (LoginSerializer)
from rest_framework.views import APIView
from django.contrib.auth import (
    logout as django_logout
)
from django.core.exceptions import ObjectDoesNotExist
from rest_auth.utils import jwt_encode


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, ]


class CustomRegisterView(RegisterView):
    """
    CustomRegisterView class for django-rest-auth
    that extends RegisterView. Create function is
    overriden to return a more detailed response
    """
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):

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


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):

        access_token = request.data.get("token", None)
        if access_token:
            return self.google_login(access_token)
        else:
            self.request = request
            self.serializer = self.get_serializer(data=self.request.data,
                                                  context={'request': request})
            if self.serializer.is_valid():
                self.user = self.serializer.validated_data['user']
                return self.login()
            else:
                return Response({"error": "Unable to Login with Provided Credentials", "Success": False})

    def google_login(self, access_token):
        payload = {'access_token': access_token}
        response = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        google_api_response = json.loads(response.text)

        if 'error' in google_api_response:
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
            return self.login()

        except Exception as err:
            return Response({"error": "Unable to Login with Provided Credentials", "Success": False})

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


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]

    def create(self, request, **kwargs):

        number_of_users = User.objects.filter(
            groups__name='Employee').count()
        if number_of_users > MAX_EMPLOYEES:
            return Response({'data': {}, 'Success': False, 'Error': 'Employees Limit Exceeded'}, status.HTTP_200_OK)
        data = request.data
        groups = data.get("role")
        password1 = data.pop("password1")
        password2 = data.pop("password2")
        if password1 != password2:
            return Response({'data': {}, 'Success': False, 'Error': 'Password not matched'}, status.HTTP_200_OK)
        data['password'] = password1
        user = UserSerializer(data=data)
        if user.is_valid():
            user.save(groups=groups)
            return Response({'data': user.data, 'Success': True, 'Error': ''}, status.HTTP_200_OK)
        else:
            return Response({'data': {}, 'Success': False, 'Error': user.errors}, status.HTTP_200_OK)

    def list(self, request):
        groups = request.query_params.get('groups', None)

        if groups:
            users = User.objects.filter(groups__name=groups)
        else:
            users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response({'data': serializer.data, "error": '', "Success": False})


class LogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.
    Accepts/Returns nothing.
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        response = self.logout(request)
        return response

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        django_logout(request)
        response = Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)
        return response
