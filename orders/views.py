from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializer import OrdersSerializer, OrderItemsSerializer
from .models import Orders, OrderItems


@permission_classes([IsAuthenticated])
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    def create(self, request, **kwargs):
        try:
            data = request.data
            order_type = data.get('type', None)
            if order_type == 'place_order':
                data.pop("type")
                order_exists = Orders.objects.filter(
                    order_by=request.user, is_checkedout=False).update(**data)
            else:

                order_item = data.pop('order_items', None)
                order_exists = Orders.objects.filter(
                    order_by=request.user, is_checkedout=False).order_by('-id').first()
                if not order_exists:
                    data['order_by'] = request.user
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
            serializer = OrdersSerializer(order_exists)
            return Response({'data': serializer.data})
        except Exception as e:
            print(e)
            return Response({'data': {}, 'error': str(e)})

    def list(self, request, **kwargs):
        listing_type = request.query_params.get('type', None)
        if listing_type:
            orders = Orders.objects.filter(
                is_checkedout=False).order_by('-id')
        else:
            if request.user.groups.filter(name='Customer').exists():
                orders = Orders.objects.filter(
                    order_by=request.user.id).exclude(is_checkedout=False).order_by('-id')
            else:
                orders = Orders.objects.all().exclude(is_checkedout=False).order_by('-id')

        serializer = OrdersSerializer(orders, many=True)
        return Response({'data': serializer.data})
