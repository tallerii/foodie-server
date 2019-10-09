from rest_framework import permissions

class ItemPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj=None):
        return obj.order.delivery_user == request.user or obj.order.client_user == request.user

class OrderPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj=None):
        return obj.delivery_user == request.user or obj.client_user == request.user
