from rest_framework import permissions


class UsersPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True

        if view.action == 'create' or view.action == 'metadata' or \
           view.action == 'password_recovery' or view.action == 'password_reset':
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj=None):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj
