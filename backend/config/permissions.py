"""
DRF Permissions
"""

from rest_framework import permissions


class IsPartner(permissions.BasePermission):
    """Allow access to partners with valid API key"""
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsCompanyOwner(permissions.BasePermission):
    """Allow access only to company owners"""
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)
