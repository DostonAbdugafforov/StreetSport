from rest_framework import serializers
from .models import Payment
from bookings.serializers import BookingSerializer


class PaymentSerializer(serializers.ModelSerializer):
    booking_details = BookingSerializer(source='booking', read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'booking', 'booking_details', 'amount', 'payment_type',
                  'status', 'transaction_id', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
