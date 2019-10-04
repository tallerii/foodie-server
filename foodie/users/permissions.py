from rest_framework import permissions


class UsersPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return True

        return request.user.is_authenticated
