from datetime import datetime

from rest_framework import viewsets, mixins, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_gis.filters import DistanceToPointFilter

from .models import User
from .permissions import UsersPermissions
from .serializers import CreateUserSerializer, PrivateUserSerializer, PublicUserSerializer, PasswordSerializer

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
    queryset = User.objects.filter(is_delivery=True)
    serializer_class = PublicUserSerializer
    distance_filter_field = 'last_location'
    filter_backends = (DistanceToPointFilter, )
