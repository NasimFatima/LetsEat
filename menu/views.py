from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import MenuItemSerializer, ItemSizeSerializer, MenuItemSerializerForHeader
from .models import MenuItems, ItemsCategory, ItemSize


@permission_classes([IsAuthenticated])
class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializer
    filterset_fields = ['id', 'name']

    def create(self, request, **kwargs):
        try:
            data = request.data
            item_categories = data.pop('item_categories', None)
            item_sizes_array = []
            menu_item, created = MenuItems.objects.get_or_create(**data)
            if item_categories:
                item_categories = [dict(item, menu_item=menu_item)
                                   for item in item_categories]
                for item_category in item_categories:
                    item_sizes = item_category.pop('item_sizes', None)
                    category_created, created = ItemsCategory.objects.get_or_create(
                        **item_category)
                    if item_sizes:
                        item_sizes = [dict(item, item_category=category_created.id)
                                      for item in item_sizes]
                if item_sizes:
                    item_sizes_array.extend(item_sizes)
                    serializer = ItemSizeSerializer(
                        data=item_sizes_array, many=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            serializer = MenuItemSerializer(menu_item)
            return Response({'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': {}, 'error': str(e)})


@permission_classes([IsAuthenticated])
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializerForHeader
