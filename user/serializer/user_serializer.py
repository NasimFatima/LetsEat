from rest_auth.registration.serializers import (RegisterSerializer,
                                                get_adapter, setup_user_email)
from rest_framework import serializers

from ..models import User
from .group_serializer import GroupSerializer


class CustomRegisterSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    address = serializers.CharField(required=False, write_only=True)

    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    role = serializers.IntegerField(required=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):

        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'address': self.validated_data.get('address', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'role': self.validated_data.get('role', ''),
        }

    def save(self, request):
        role = request.data['role']
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        if role == -1:
            user.is_superuser = True
        else:
            user.is_superuser = False
            user.role = role
            user.groups.add(role)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    # Because User and Group are in many-to-many relations so you can directly add the
    # group field in the users serializers. For more details follow django.contrib.auth.models
    # package and User inherits AbstactUser and AbstractUser inherits PermissionsMixin
    # which has groups as many to many field.

    class Meta:

        model = User
        groups = GroupSerializer(many=True)
        fields = ('pk', 'username', 'email', 'first_name', 'last_name',
                  'phone',  'is_superuser', 'role', 'groups')
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1
