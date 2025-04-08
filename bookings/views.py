from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for bookings
    - Users can create bookings and manage their own bookings
    - Stadium owners can view bookings for their stadiums
    - Stadium managers can view and update bookings for their stadiums
    - Admins can see and manage all bookings
    """
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['booking_date', 'start_time', 'created_at', 'status']

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Booking.objects.none()

        if user.role == 'ADMIN':
            # Admins see all bookings
            return Booking.objects.all()

        if user.role == 'STADIUM_OWNER':
            # Stadium owners see bookings for their stadiums
            return Booking.objects.filter(stadium__owner=user)

        if user.role == 'STADIUM_MANAGER':
            # Stadium managers see bookings for stadiums they manage
            managed_stadium_ids = user.managed_stadiums.filter(
                is_active=True
            ).values_list('stadium_id', flat=True)

            return Booking.objects.filter(stadium_id__in=managed_stadium_ids)

        # Regular users see only their own bookings
        return Booking.objects.filter(user=user)

    def get_permissions(self):
        """
        - List and retrieve: Any authenticated user (filtered by role)
        - Create: Regular users
        - Update: Regular users (their own), Stadium managers, or Admins
        - Delete: Regular users (their own) or Admins
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Set the user to the current user
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Special permission check for updates
        user = request.user
        if not (user.is_admin or
                instance.user == user or
                (user.is_stadium_manager and
                 user.managed_stadiums.filter(
                     stadium=instance.stadium, is_active=True
                 ).exists())):
            return Response(
                {"detail": "You do not have permission to modify this booking."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking (for stadium managers)"""
        booking = self.get_object()

        # Check if user is the stadium manager for this stadium
        user = request.user
        if not (user.is_admin or
                (user.is_stadium_manager and
                 user.managed_stadiums.filter(
                     stadium=booking.stadium, is_active=True
                 ).exists())):
            return Response(
                {"detail": "Only stadium managers can confirm bookings."},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status != 'PENDING':
            return Response(
                {"detail": f"Booking is already {booking.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'CONFIRMED'
        booking.save()

        return Response({"detail": "Booking confirmed successfully."})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a booking as completed (for stadium managers)"""
        booking = self.get_object()

        # Check if user is the stadium manager for this stadium
        user = request.user
        if not (user.is_admin or
                (user.is_stadium_manager and
                 user.managed_stadiums.filter(
                     stadium=booking.stadium, is_active=True
                 ).exists())):
            return Response(
                {"detail": "Only stadium managers can complete bookings."},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status not in ['PENDING', 'CONFIRMED']:
            return Response(
                {"detail": f"Cannot complete a booking with status {booking.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'COMPLETED'
        booking.save()

        return Response({"detail": "Booking marked as completed."})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()

        # Users can cancel their own bookings
        # Stadium managers can cancel bookings for their stadiums
        # Admins can cancel any booking
        user = request.user

        if not (user.is_admin or
                booking.user == user or
                (user.is_stadium_manager and
                 user.managed_stadiums.filter(
                     stadium=booking.stadium, is_active=True
                 ).exists())):
            return Response(
                {"detail": "You do not have permission to cancel this booking."},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status not in ['PENDING', 'CONFIRMED']:
            return Response(
                {"detail": f"Cannot cancel a booking with status {booking.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'CANCELLED'
        booking.save()

        return Response({"detail": "Booking cancelled successfully."})



