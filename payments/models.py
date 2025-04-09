from django.db import models
from bookings.models import Booking


class PaymentType:
    CASH = 'cash'
    ONLINE = 'online'

    CHOICES = (
        (CASH, 'Cash'),
        (ONLINE, 'Online'),
    )


class PaymentStatus:
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

    CHOICES = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    )


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PaymentType.CHOICES)
    status = models.CharField(max_length=10, choices=PaymentStatus.CHOICES, default=PaymentStatus.PENDING)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for booking {self.booking.id}"


