from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from .permissions import UsersPermissions
from .serializers import CreateUserSerializer, PrivateUserSerializer, PublicUserSerializer
from datetime import datetime

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    permission_classes = (UsersPermissions,)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if ((self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update') and \
           self.request.user == self.get_object()) or self.action == 'self':
            return PrivateUserSerializer
        return PublicUserSerializer

    def create(self, request, is_delivery):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save(is_delivery=is_delivery)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=request.data)
        if serializer.is_valid():
            serializer.save(location_last_updated=datetime.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=request.data)
        if serializer.is_valid():
            if 'lat' in serializer.validated_data or 'lon' in serializer.validated_data:
                serializer.save(location_last_updated=datetime.now())
            else:
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'patch', 'put', 'delete'])
    def self(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.user.pk

        if request.method == 'GET':
            return self.retrieve(request, args, kwargs)
        elif request.method == 'PUT':
            return self.update(request, args, kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, args, kwargs)
        elif request.method == 'DELETE':
            return self.destroy(request, args, kwargs)


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
