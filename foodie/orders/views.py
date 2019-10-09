# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

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
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, is_delivery):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_error=True)

        serializer.save(client_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ItemViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (ItemPermissions,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
