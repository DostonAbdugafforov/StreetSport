from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Stadium, StadiumImage, StadiumManager, SportType, Amenity


class SportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportType
        fields = ('id', 'name')


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('id', 'name')


class StadiumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumImage
        fields = ('id', 'image', 'is_primary')


class StadiumManagerSerializer(serializers.ModelSerializer):
    manager_details = UserSerializer(source='manager', read_only=True)

    class Meta:
        model = StadiumManager
        fields = ('id', 'manager', 'manager_details', 'is_active')


class StadiumSerializer(serializers.ModelSerializer):
    images = StadiumImageSerializer(many=True, read_only=True)
    sport_types = SportTypeSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    owner_details = UserSerializer(source='owner', read_only=True)
    managers = StadiumManagerSerializer(many=True, read_only=True)

    class Meta:
        model = Stadium
        fields = ('id', 'name', 'address', 'description', 'price_per_hour',
                  'opening_time', 'closing_time', 'owner', 'owner_details',
                  'sport_types', 'amenities', 'images', 'managers',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner_details')
