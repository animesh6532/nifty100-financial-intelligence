# Partner API permissions
from rest_framework.permissions import BasePermission


class IsPartner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'api_key'))
