from rest_framework import serializers
from .models import Booking
from stadiums.serializers import StadiumSerializer
from accounts.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    stadium_details = StadiumSerializer(source='stadium', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'stadium', 'stadium_details', 'user', 'user_details',
                  'date', 'start_time', 'end_time', 'status', 'total_price',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'total_price', 'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Calculate total price based on booking duration and stadium price
        stadium = validated_data['stadium']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']

        # Calculate duration in hours
        duration_hours = (end_time.hour - start_time.hour) + (end_time.minute - start_time.minute) / 60
        validated_data['total_price'] = stadium.price_per_hour * duration_hours

        return super().create(validated_data)
