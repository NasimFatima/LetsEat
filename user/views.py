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
from .services.loginService import login
from django.contrib.auth.models import Group
from .serializer import GroupSerializer
from rest_framework.generics import GenericAPIView
from rest_auth.serializers import (LoginSerializer)
from rest_framework.views import APIView
from django.contrib.auth import (
    logout as django_logout
)
from django.core.exceptions import ObjectDoesNotExist


@permission_classes([IsAuthenticated])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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
            return Response({"error": str(err), "Success": False})


@permission_classes([AllowAny])
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        try:
            self.request = request
            self.serializer = self.get_serializer(data=self.request.data,
                                                  context={'request': request})
            self.serializer.is_valid(raise_exception=True)
            self.user = self.serializer.validated_data['user']
            response = login(self)
        except Exception as err:
            return Response({"error": "Unable to Login with Provided Credentials", "Success": False})
        return response


@permission_classes([AllowAny])
class GoogleView(GenericAPIView):
    serializer_class = LoginSerializer

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
            response = login(self)
            return response
        except Exception as err:
            return Response({"error": "Unable to Login with Provided Credentials", "Success": False})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, **kwargs):
        try:
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
        except Exception as e:
            return Response({'data': {}, 'Success': False, 'Error': str(e)}, status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class LogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.
    Accepts/Returns nothing.
    """
    permission_classes = (IsAuthenticated)

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
