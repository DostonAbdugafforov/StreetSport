from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsAdmin
from bookings.models import Booking
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for payments
    - Users can create and view their own payments
    - Stadium managers can record cash payments
    - Stadium owners can view payments for their stadiums
    - Admins can see and manage all payments
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Payment.objects.none()

        if user.role == 'ADMIN':
            # Admins see all payments
            return Payment.objects.all()

        if user.role == 'STADIUM_OWNER':
            # Stadium owners see payments for their stadiums
            return Payment.objects.filter(booking__stadium__owner=user)

        if user.role == 'STADIUM_MANAGER':
            # Stadium managers see payments for stadiums they manage
            managed_stadium_ids = user.managed_stadiums.filter(
                is_active=True
            ).values_list('stadium_id', flat=True)

            return Payment.objects.filter(
                Q(booking__stadium_id__in=managed_stadium_ids) |
                Q(received_by=user)
            )

        # Regular users see only their own payments
        return Payment.objects.filter(booking__user=user)

    def get_permissions(self):
        """
        - List and retrieve: Any authenticated user (filtered by role)
        - Create: Regular users, Stadium managers
        - Update: Not allowed for anyone except admins
        - Delete: Not allowed for anyone except admins
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def record_cash_payment(self, request):
        """Record a cash payment (for stadium managers)"""
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')

        if not booking_id or not amount:
            return Response(
                {"detail": "Booking ID and amount are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user is the stadium manager for this stadium
        user = request.user
