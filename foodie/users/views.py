from rest_framework import viewsets, mixins
from .models import User
from .permissions import UsersPermissions
from .serializers import CreateUserSerializer, UserSerializer, PublicUserSerializer
from django_filters.rest_framework import DjangoFilterBackend

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

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicUserSerializer
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer
