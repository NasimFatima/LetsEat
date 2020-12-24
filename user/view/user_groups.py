from rest_framework import status, viewsets
from django.contrib.auth.models import Group, ContentType
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view
from ..serializer.group_serializer import GroupSerializer


@permission_classes([AllowAny])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
