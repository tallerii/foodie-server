from rest_framework import permissions


class OrderPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'metadata':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj=None):
        return obj.delivery_user == request.user or obj.client_user == request.user


class UnassignedOrderPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'metadata':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj=None):
        return request.user.is_delivery
