from rest_framework import mixins, viewsets

from foodie.orders.models import Order, UNASSIGNED_STATUS, IN_PROGRESS_STATUS
from foodie.orders.permissions import OrderPermissions, UnassignedOrderPermissions
from foodie.orders.serializers import ListOrdersSerializer, ActivateOrdersSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [OrderPermissions]
    serializer_class = ListOrdersSerializer

    def get_queryset(self):
        if self.request.user.is_delivery:
            return self.request.user.delivered_orders.all()
        else:
            return self.request.user.orders_made.all()

    def perform_create(self, serializer):
        serializer.save(client_user=self.request.user)


class ActiveOrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [OrderPermissions]
    serializer_class = ListOrdersSerializer
    queryset = Order.objects.filter(status=IN_PROGRESS_STATUS)


class UnassignedOrderViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = [UnassignedOrderPermissions]
    serializer_class = ActivateOrdersSerializer
    queryset = Order.objects.filter(status=UNASSIGNED_STATUS)

    def perform_update(self, serializer):
        serializer.save(delivery_user=self.request.user, status=IN_PROGRESS_STATUS)
