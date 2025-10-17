# tasks/permissions.py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission: only owners or staff users can edit/delete; read is allowed to anyone.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to owner or staff
        return obj.owner == request.user or request.user.is_staff
