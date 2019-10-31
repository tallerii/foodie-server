from rest_framework import mixins, viewsets

from foodie.orders.permissions import OrderPermissions
from foodie.orders.serializers import ListOrdersSerializer


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
