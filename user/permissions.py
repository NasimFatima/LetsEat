from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Admin').exists()

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.groups.filter(name='Admin').exists()
