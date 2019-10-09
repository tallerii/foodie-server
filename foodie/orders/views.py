from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from foodie.orders.models import Product, Order, Item
from foodie.orders.serializers import ProductSerializer, ItemSerializer, OrderSerializer
from foodie.orders.permissions import ItemPermissions, OrderPermissions


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (OrderPermissions,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_delivery:
            queryset = self.request.user.delivered_orders.all()
        else:
            return self.request.user.orders_made.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(client_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ItemViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (ItemPermissions,)
    serializer_class = ItemSerializer
