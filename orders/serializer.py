from rest_framework import serializers
from .models import Orders, OrderItems


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'
        depth = 3


class OrdersSerializer(serializers.ModelSerializer):
    order = OrderItemsSerializer(many=True)

    class Meta:
        model = Orders
        fields = ('id', 'created_at', 'payment_method',
                  'total_bill', 'order_by', 'order_number', 'order')
        depth = 2
