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
from drf_spectacular.utils import extend_schema


# Decorador para documentar las vistas de la API
@extend_schema(
    summary="Registro de usuario",
    description="Permite registrar un nuevo usuario en el sistema.",
)
# Registrar un usuario
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


@extend_schema(
    summary="Inicio de sesión",
    description="Permite a un usuario autenticarse y obtener un token JWT.",
)
# Iniciar sesión
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    summary="Cerrar sesión",
    description="Permite a un usuario cerrar sesión y revocar su token.",
)
# Cerrar sesión
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


@extend_schema(
    summary="Solicitar restablecimiento de contraseña",
    description="Envía un correo electrónico al usuario con instrucciones para restablecer su contraseña.",
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


@extend_schema(
    summary="Confirmar restablecimiento de contraseña",
    description="Permite al usuario establecer una nueva contraseña utilizando el token recibido por correo electrónico.",
)
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
