from rest_framework import permissions


class UsersPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if view.action == 'list':
            return request.user

        if view.action == 'create':
            return True

        return obj == request.user
