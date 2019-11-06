from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from foodie.orders.models import Order, UNASSIGNED_STATUS, IN_PROGRESS_STATUS, DELIVERED_STATUS
from foodie.orders.serializers import ListOrdersSerializer, CreateOrderSerializer

from firebase_admin import messaging


class OrderViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return ListOrdersSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')

        if status == UNASSIGNED_STATUS:
            return Order.objects.filter(status=status)

        if status == IN_PROGRESS_STATUS or status == DELIVERED_STATUS:
            if self.request.user.is_delivery:
                return self.request.user.delivered_orders.filter(status=status)
            else:
                return self.request.user.orders_made.filter(status=status)

        if self.request.user.is_delivery:
            return self.request.user.delivered_orders.all()
        else:
            return self.request.user.orders_made.all()

    def perform_create(self, serializer):
        serializer.save(client_user=self.request.user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status == UNASSIGNED_STATUS:
            newStatus = IN_PROGRESS_STATUS
        elif order.status == IN_PROGRESS_STATUS or order.status == DELIVERED_STATUS:
            newStatus = DELIVERED_STATUS
        elif DELIVER_ERROR_STATUS:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        order.status = newStatus
        order.save()
        notify_client(newStatus, order.client_user, order.delivery_user)
        return Response(data=order, status=status.HTTP_200_OK)

    def notify_client(self, newStatus, client, delivery):
        message = messaging.Message(
            data={
                'status': newStatus,
                'delivery': str(delivery.id)
            },
            token=str(client.FCMToken),
        )
        try:
            response = messaging.send(message)
        except:
            # TODO: handle message error
            print('Firebase messaging error')
