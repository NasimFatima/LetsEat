from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .serializers import MenuItemSerializer, ItemSizeSerializer, MenuItemSerializerForHeader
from .models import MenuItems, ItemsCategory, ItemSize


class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializer
    filterset_fields = ['id', 'name']

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(MenuViewSet, self).get_permissions()

    def create(self, request, **kwargs):
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
                if serializer.is_valid():
                    serializer.save()
        serializer = MenuItemSerializer(menu_item)
        return Response({'data': serializer.data}, status.HTTP_200_OK)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializerForHeader

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(MenuItemViewSet, self).get_permissions()
