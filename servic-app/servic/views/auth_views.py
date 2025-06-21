from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from django.db import IntegrityError
from django.conf import settings
from ..serializers import (
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
    LogoutSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


# Aqui definimos la logica de la API similar al archivo "usersController.js"
# Creamos las funciones que vamos a usar en la API
# Crear un usuario


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            return Response(
                {"email": ["El email ya está registrado."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Usuario registrado exitosamente",
            },
            status=status.HTTP_201_CREATED,
        )


# Loguear un usuario


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Cerrar sesión de un usuario
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Sesión cerrada exitosamente"}, status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"detail": "Token de actualización inválido"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Recuperar contraseña - Solicitud
class PasswordResetRequestView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        response = {
            "message": "Si el email está registrado, se ha generado un token de reseteo."
        }
        if settings.DEBUG:
            response.update({"uid": data["uid"], "token": data["token"]})
        return Response(response, status=status.HTTP_200_OK)


# Recuperar contraseña - Confirmación
class PasswordResetConfirmView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "La contraseña ha sido restablecida exitosamente."},
            status=status.HTTP_200_OK,
        )
