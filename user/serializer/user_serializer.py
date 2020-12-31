from rest_framework import serializers

from ..models import User
from .group_serializer import GroupSerializer


class UserSerializer(serializers.ModelSerializer):

    # Because User and Group are in many-to-many relations so you can directly add the
    # group field in the users serializers. For more details follow django.contrib.auth.models
    # package and User inherits AbstactUser and AbstractUser inherits PermissionsMixin
    # which has groups as many to many field.

    class Meta:

        model = User
        groups = GroupSerializer(many=True)
        fields = ('pk', 'username', 'email', 'first_name', 'last_name',
                  'phone',  'is_superuser', 'groups', 'password')
        depth = 1

    def create(self, validated_data):
        group = validated_data.pop('groups')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.groups.add(group)
        user.set_password(password)
        user.save()
        return user
