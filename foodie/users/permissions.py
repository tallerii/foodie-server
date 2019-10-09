from rest_framework import permissions


class UsersPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if view.action == 'create' or view.action == 'metadata':
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj=None):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj
