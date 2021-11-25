from rest_framework import permissions


class IsOwn(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnAccount(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
