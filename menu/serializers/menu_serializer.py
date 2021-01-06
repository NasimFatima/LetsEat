from rest_framework import serializers
from ..models import MenuItems, ItemsCategory, ItemSize


class ItemSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSize
        fields = '__all__'


class ItemsCategorySerializer(serializers.ModelSerializer):
    item_category = ItemSizeSerializer(many=True, read_only=True)

    class Meta:
        model = ItemsCategory
        fields = (
            'id', 'name', 'description', 'item_category'
        )


class MenuItemSerializer(serializers.ModelSerializer):
    item = ItemsCategorySerializer(many=True, required=False)

    class Meta:
        model = MenuItems
        fields = ('id', 'name', 'item')


class MenuItemSerializerForHeader(serializers.ModelSerializer):

    class Meta:
        model = MenuItems
        fields = ('id', 'name', 'item')
