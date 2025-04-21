from decimal import Decimal

from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'stadium', 'user',
                  'date', 'start_time', 'end_time',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Calculate total price based on booking duration and stadium price
        stadium = validated_data['stadium']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']

        # Calculate duration in hours
        duration_hours = (end_time.hour - start_time.hour) + (end_time.minute - start_time.minute) / 60
        validated_data['total_price'] = stadium.price_per_hour * Decimal(duration_hours)

        return super().create(validated_data)
