from rest_framework import serializers
from .models import Orders, OrderItems


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class OrderItemsSerializerForListing(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'
        depth = 3


class OrdersSerializer(serializers.ModelSerializer):

    def get_payment_method(self, obj):
        choices = Orders.PAYMENT_METHOD_CHOICES_DICT
        if obj.payment_method is not None:
            payment_method = choices[obj.payment_method]
        else:
            payment_method = ""
        return payment_method

    order = OrderItemsSerializerForListing(many=True)
    payment_method = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('id', 'created_at', 'payment_method',
                  'total_bill', 'order_by',  'order', 'status')
        depth = 2
