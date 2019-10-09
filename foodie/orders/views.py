# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from foodie.orders.models import Product, Order, Item
from foodie.orders.serializers import ProductSerializer, ItemSerializer, OrderSerializer


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get', 'put', 'delete', 'post'])
    def self(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.retrieve(request, args, kwargs)
        elif request.method == 'PUT':
            return self.update(request, args, kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, args, kwargs)
        elif request.method == 'POST':
            return self.create(request, args, kwargs)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['get', 'put', 'delete', 'post'])
    def self(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.retrieve(request, args, kwargs)
        elif request.method == 'PUT':
            return self.update(request, args, kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, args, kwargs)
        elif request.method == 'POST':
            return self.create(request, args, kwargs)



class ItemViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=False, methods=['get', 'put', 'delete', 'post'])
    def self(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.retrieve(request, args, kwargs)
        elif request.method == 'PUT':
            return self.update(request, args, kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, args, kwargs)
        elif request.method == 'POST':
            return self.create(request, args, kwargs)
