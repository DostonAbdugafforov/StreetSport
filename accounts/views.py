from django.contrib.auth import authenticate
from drf_yasg import openapi
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer, UserRegisterSerializer


class SignUpView(APIView):
    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Foydalanuvchi profilini ko‘rish
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request):
        # Foydalanuvchi profilini tahrirlash
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, example='oldpass123'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, example='newpass456'),
            },
        )
    )
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Eski parolni tekshirish
        user = authenticate(username=request.user.username, password=old_password)
        if user:
            if new_password:
                request.user.set_password(new_password)
                request.user.save()
                return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
            return Response({"detail": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
