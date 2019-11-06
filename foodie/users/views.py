import secrets
from datetime import datetime

from django.core.mail import send_mail
from rest_framework import viewsets, mixins, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_gis.filters import DistanceToPointFilter

from .models import User
from .permissions import UsersPermissions
from .serializers import CreateUserSerializer, PrivateUserSerializer, PublicUserSerializer, PasswordSerializer, \
    RecuperationTokenSerializer

from firebase_admin import db as firebaseDB


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
        if self.action == 'set_password':
            return PasswordSerializer
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

        self.update_location_to_firebase(serializer.validated_data)
        serializer.save(location_last_updated=datetime.now())
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'last_location' in serializer.validated_data:
            self.update_location_to_firebase(serializer.validated_data)
            serializer.save(location_last_updated=datetime.now())
        else:
            serializer.save()
        return Response(serializer.data)

    def update_location_to_firebase(self, validated_data):
        ref = firebaseDB.reference('users')
        users_ref = ref.child(str(self.get_object().id))
        users_ref.set({
            'lat': validated_data.get('last_location').x,
            'lon': validated_data.get('last_location').y
        })


class DeliveryViewSet(UserViewSet):
    """
    Updates and retrieves deliveries
    """
    queryset = User.objects.filter(is_delivery=True)

    def create(self, request, *args, **kwargs):
        return super().create(request, is_delivery=True)


class ClientViewSet(UserViewSet):
    """
    Updates and retrieves clients
    """
    queryset = User.objects.filter(is_delivery=False)

    def create(self, request, *args, **kwargs):
        return super().create(request, is_delivery=False)


class NearDeliveryList(ListAPIView, viewsets.GenericViewSet):
    """
    The dist parameter is implicit:
    /near_deliveries/?dist=radious&point=x,y&format=json
    """
    permission_classes = (UsersPermissions,)
    queryset = User.objects.filter(is_delivery=True)
    serializer_class = PublicUserSerializer
    distance_filter_field = 'last_location'
    filter_backends = (DistanceToPointFilter, )


class PasswordRecoveryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (UsersPermissions,)
    serializer_class = RecuperationTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        recuperation_token = secrets.token_urlsafe(14)
        serializer.save(recuperation_token=recuperation_token)
        send_mail(
            'Recovery token',
            "Your recovery token is %s" % recuperation_token,
            'foodie_helpdesk@sandbox3889059f07594dbb84189d1d99bbed1b.mailgun.org',
            [self.request.user.email],
            fail_silently=False,
        )
        return Response(data="Your recovery token was send to %s" % self.request.user.email, status=status.HTTP_200_OK)
