from rest_framework import viewsets

from foodie.orders.permissions import OrderPermissions
from foodie.orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [OrderPermissions]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_delivery:
            return self.request.user.delivered_orders.all()
        else:
            return self.request.user.orders_made.all()

    def perform_create(self, serializer):
        serializer.save(client_user=self.request.user)
