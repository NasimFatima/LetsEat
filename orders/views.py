from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializer import OrdersSerializer, OrderItemsSerializer
from .models import Orders, OrderItems
from rest_framework.decorators import action


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, **kwargs):
        data = request.data
        order_type = data.get('type', None)
        if order_type == 'place_order':
            data.pop("type")
            order_exists = Orders.objects.filter(
                customer=request.user, is_checkedout=False).first()
            order_exists.is_checkedout = True
            order_exists.save()
        else:

            order_item = data.pop('order_items', None)
            order_exists = Orders.objects.filter(
                customer=request.user, is_checkedout=False).order_by('-id').first()

            if not order_exists:
                data['customer'] = request.user
                order_exists = Orders.objects.create(**data)
            else:
                order_exists.total_bill = order_exists.total_bill + \
                    data['total_bill']
                order_exists.save()
            order_item_exists = OrderItems.objects.filter(
                order=order_exists.id, item_category=order_item['item_category']).first()

            if order_item_exists:

                if order_item['quantity'] > 0:
                    order_item_exists.quantity = order_item['quantity']
                    order_item_exists.save()
                else:
                    order_item_exists.delete()

            else:
                order_item['order'] = order_exists.id
                serializer = OrderItemsSerializer(data=order_item)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        serializer = self.get_serializer(order_exists)
        return Response({'data': serializer.data})

    def list(self, request, **kwargs):

        if request.user.groups.filter(name='Customer').exists():
            orders = Orders.objects.filter(
                customer=request.user.id).exclude(is_checkedout=False).order_by('-id')
        else:
            orders = Orders.objects.all().exclude(is_checkedout=False).order_by('-id')

        serializer = self.get_serializer(orders, many=True)
        return Response({'data': serializer.data})

    @action(detail=False)
    def cart_items(self, request):

        orders = Orders.objects.filter(
            is_checkedout=False, customer=request.user.id).order_by('-id')
        serializer = self.get_serializer(orders, many=True)
        return Response({'data': serializer.data})

    @action(detail=True, methods=['post'])
    def change_order_status(self, request, pk=None):

        order = Orders.objects.filter(id=pk).first()
        order.status = request.data['status']
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
