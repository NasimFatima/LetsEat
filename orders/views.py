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
            data['order_by'] = request.user
            order_items = data.pop('order_items', None)
            order = Orders.objects.create(**data)
            if order_items:
                order_items = [dict(item, order=order.id)
                               for item in order_items]
                serializer = OrderItemsSerializer(data=order_items, many=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            serializer = OrdersSerializer(order)
            return Response({'data': serializer.data})
        except Exception as e:
            print(e)
            return Response({'data': {}, 'error': str(e)})

    def list(self, request, **kwargs):
        if request.user.groups.filter(name='Customer').exists():
            orders = Orders.objects.filter(
                order_by=request.user.id).order_by('-id')
        else:
            orders = Orders.objects.all().order_by('-id')

        serializer = OrdersSerializer(orders, many=True)
        return Response({'data': serializer.data})
