import random
from datetime import timedelta

from django.db.models import Q
from firebase_admin import messaging, exceptions
from rest_framework import mixins, viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodie.orders.models import Order, UNASSIGNED_STATUS, IN_PROGRESS_STATUS, DELIVERED_STATUS, DELIVER_ERROR_STATUS
from foodie.orders.serializers import ListOrdersSerializer, CreateOrderSerializer

DELIVERY_PERCENTAGE_FEE = 0.85


class OrderViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        if self.action == 'update':
            return serializers.Serializer
        return ListOrdersSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')

        if status == UNASSIGNED_STATUS:
            return Order.objects.filter(status=status)

        if status == IN_PROGRESS_STATUS or status == DELIVERED_STATUS:
            if self.request.user.is_delivery:
                return self.request.user.delivered_orders.filter(status=status)
            return self.request.user.orders_made.filter(status=status)

        if self.request.user.is_delivery:
            return Order.objects.filter(Q(delivery_user=self.request.user) | Q(status=UNASSIGNED_STATUS))
        else:
            return self.request.user.orders_made.all()

    def perform_create(self, serializer):
        serializer.save(client_user=self.request.user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = order.status
        if order.status == UNASSIGNED_STATUS:
            if not request.user.is_delivery:
                return Response(
                    {'error': 'only a delivery user can self-assign an order'},
                    status=status.HTTP_400_BAD_REQUEST)
            new_status = IN_PROGRESS_STATUS
            order.delivery_price = round(random.uniform(10, 100), 2)
            order.delivery_user = request.user
        elif order.status == IN_PROGRESS_STATUS:
            new_status = DELIVERED_STATUS
            order.delivery_user.balance += DELIVERY_PERCENTAGE_FEE * order.delivery_price
            order.delivery_user.save()      
        elif order.status == DELIVER_ERROR_STATUS:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        self.notify_client(new_status, order.client_user, order.delivery_user)
        return Response(status=status.HTTP_200_OK)

    def notify_client(self, new_status, client, delivery):
        # [START android_message]
        message = messaging.Message(
            android=messaging.AndroidConfig(
                ttl=timedelta(seconds=3600),
                priority='normal',
                notification=messaging.AndroidNotification(
                    title='Cambio de estado',
                    body=str(new_status)
                ),
                data={
                    'status': str(new_status),
                    'delivery': str(delivery.id)
                }
            ),
            token=str(client.FCMToken),	
        )
        # [END android_message]
        try:
            response = messaging.send(message)
        except exceptions.FirebaseError as e:
            print('Firebase messaging error: ' + str(e))


