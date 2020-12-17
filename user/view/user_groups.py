from rest_framework import status, viewsets
from django.contrib.auth.models import Group, ContentType
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view
from ..serializer.group_serializer import GroupSerializer


@api_view()
@permission_classes([AllowAny])
def get_all_roles(request):
    try:
        groups = Group.objects.all().order_by('id')
        serializer = GroupSerializer(groups, many=True)
        data = list(serializer.data)
        data.append({'id': -1, 'name': "Super User"})
        res = {"Success": True, "data": data}
        return Response(res, status.HTTP_200_OK)
    except Exception as e:
        print("EXCEPTION list GroupViewSet: ", e)
        return Response({"Success": False, "data": []}, status.HTTP_200_OK)
