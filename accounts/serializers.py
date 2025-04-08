from rest_framework import serializers
from .models import User, UserRole


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'phone', 'role', 'created_at')
        read_only_fields = ('id', 'created_at')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'phone', 'password', 'role')
        extra_kwargs = {'role': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['username'],
            phone=validated_data.get('phone', ''),
            password=validated_data['password'],
            role=UserRole.USER
        )
        return user
