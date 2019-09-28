from rest_framework import status, viewsets, mixins
from .models import User
from .permissions import UsersPermissions
from .serializers import CreateUserSerializer, PrivateUserSerializer, PublicUserSerializer, LocationUserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    permission_classes = (UsersPermissions,)
    filter_backends = [DjangoFilterBackend]

    @action(detail=True, methods=['get', 'put'])
    def location(self, request, pk=None):
        """
        Updates and retreives user location
        """
        return self.partial_update(request, location_last_updated=datetime.now())

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicUserSerializer
        if self.action == 'create':
            return CreateUserSerializer
        if self.action == 'update' or self.action == 'retrieve':
            return PrivateUserSerializer
        if self.action == 'location':
            return LocationUserSerializer
        return PublicUserSerializer
