import secrets
from datetime import datetime

from django.core.mail import send_mail
from firebase_admin import db as firebaseDB
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_gis.filters import DistanceToPointFilter

from foodie.orders.models import Order, DELIVERED_STATUS, DELIVER_ERROR_STATUS
from .models import User
from .permissions import UsersPermissions
from .serializers import CreateUserSerializer, PrivateUserSerializer, PublicUserSerializer, PasswordResetSerializer, \
    PasswordRecuperationSerializer, PaymentSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    permission_classes = (UsersPermissions,)

    def get_object(self):
        if self.kwargs['pk'] == 'self':
            return self.request.user
        else:
            return super().get_object()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if ((self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update') and \
           self.request.user == self.get_object()):
            return PrivateUserSerializer
        if self.action == 'password_recovery':
            return PasswordRecuperationSerializer
        if self.action == 'password_reset':
            return PasswordResetSerializer
        # TODO: create admin users and uncomment the following line
        #if (self.action == 'payment' and self.request.user.is_admin):
        if self.action == 'payment':
            return PaymentSerializer
        return PublicUserSerializer

    def create(self, request, is_delivery):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(is_delivery=is_delivery)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)

        when = self.update_location_to_firebase(serializer.validated_data)
        serializer.save(location_last_updated=when)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'last_location' in serializer.validated_data:
            when = self.update_location_to_firebase(serializer.validated_data)
            serializer.save(location_last_updated=when)
        else:
            serializer.save()
        return Response(serializer.data)

    def update_location_to_firebase(self, validated_data):
        ref = firebaseDB.reference('users')
        users_ref = ref.child(str(self.get_object().id))
        now = datetime.now()
        users_ref.set({
            'lat': validated_data.get('last_location').x,
            'lon': validated_data.get('last_location').y,
            'when': now
        })
        return now

    @action(detail=False, methods=['post'])
    def password_recovery(self, request):
        serializer = PasswordRecuperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        user.recuperation_token = secrets.token_urlsafe(14)
        user.save()
        send_mail(
            'Foodie recovery token',
            'Your recovery token is %s' % user.recuperation_token,
            'foodie_helpdesk@sandbox3889059f07594dbb84189d1d99bbed1b.mailgun.org',
            [user.email],
            fail_silently=False,
        )
        return Response({'status': 'recovery token was send to %s' % user.email})

    @action(detail=False, methods=['post'])
    def password_reset(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        return Response({'status': 'new password set'})

    @action(detail=False, methods=['post'])
    def payment(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        user.balance -= serializer.validated_data.get('payment')
        user.save()
        return Response({'status': 'payment received'})

class DeliveryViewSet(UserViewSet):
    """
    Updates and retrieves deliveries
    """
    queryset = User.objects.filter(is_delivery=True)
    """
    The dist parameter is implicit:
    /near_deliveries/?dist=radious&point=x,y&format=json
    """
    distance_filter_field = 'last_location'
    filter_backends = (DistanceToPointFilter, )

    def create(self, request, *args, **kwargs):
        return super().create(request, is_delivery=True)


class ClientViewSet(UserViewSet):
    """
    Updates and retrieves clients
    """
    queryset = User.objects.filter(is_delivery=False)

    def create(self, request, *args, **kwargs):
        return super().create(request, is_delivery=False)


class StatsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Get application stats
    """
    def list(self, request, *args, **kwargs):
        return Response({'users': User.objects.count(),
                         'orders_delivered': Order.objects.filter(status=DELIVERED_STATUS).count(),
                         'orders_failed': Order.objects.filter(status=DELIVER_ERROR_STATUS).count()})
