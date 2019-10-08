from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from .permissions import UsersPermissions
from .serializers import CreateUserSerializer, PrivateUserSerializer, PublicUserSerializer, PasswordSerializer
from datetime import datetime

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

        serializer.save(location_last_updated=datetime.now())
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'lat' in serializer.validated_data or 'lon' in serializer.validated_data:
            serializer.save(location_last_updated=datetime.now())
        else:
            serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'password set'})


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
