from rest_framework import permissions

from bookings.models import Booking
from stadiums.models import Stadium
from .models import UserRole


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.ADMIN


class IsStadiumOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.STADIUM_OWNER


class IsStadiumManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.STADIUM_MANAGER


class IsStadiumOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.role == UserRole.STADIUM_OWNER or
                request.user.role == UserRole.ADMIN
        )


class IsUser(permissions.BasePermission):
    """
    Custom permission to check if the request user is the same as the user in the object.
    Also allows users to view and create bookings, and view stadiums.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user

    def has_permission(self, request, view):
        """
        Allow users to view stadiums and make bookings.
        """
        if request.user.is_authenticated:
            if view.action in ['list', 'retrieve'] and isinstance(view.queryset.model, Stadium):
                return True
            if view.action == 'create' and isinstance(view.queryset.model, Booking):
                return True
            return False
        return False
