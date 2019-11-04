from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from foodie.orders.models import Order, UNASSIGNED_STATUS, IN_PROGRESS_STATUS
from foodie.orders.permissions import OrderPermissions, UnassignedOrderPermissions
from foodie.orders.serializers import ListOrdersSerializer, ActivateOrdersSerializer

from firebase_admin import messaging

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


class UnassignedOrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [UnassignedOrderPermissions]
    serializer_class = ActivateOrdersSerializer
    queryset = Order.objects.filter(status=UNASSIGNED_STATUS)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save(delivery_user=self.request.user, status=IN_PROGRESS_STATUS)
        message = messaging.Message(
            data={
                'status': 'in progress',
                'delivery': str(self.request.user.id)
            },
            token=str(order.client_user.FCMToken),
        )
        try:
            response = messaging.send(message)
        except:
            # TODO: handle message error
            print('Firebase messaging error')

        return Response(data=serializer.data, status=status.HTTP_200_OK)
