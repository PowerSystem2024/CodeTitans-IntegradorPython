from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import User, UserRoleChangeLog
from ..serializers import (
    UserProfileSerializer,
    UserRoleChangeSerializer,
    ChangePasswordSerializer,
)
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Perfil de usuario",
    description="Permite consultar y actualizar los datos del perfil del usuario autenticado."
)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    @extend_schema(
        summary="Actualizar perfil de usuario (PUT)",
        description="Actualiza completamente todos los datos del perfil del usuario autenticado. Se deben enviar todos los campos requeridos."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar parcialmente el perfil de usuario (PATCH)",
        description="Actualiza parcialmente los datos del perfil del usuario autenticado. Solo se deben enviar los campos que se desean modificar."
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
class UserRoleChangeView(generics.UpdateAPIView):
    serializer_class = UserRoleChangeSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        return get_object_or_404(User, id=user_id)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Guardar el rol anterior
        previous_role = user.user_type

        # Realizar el cambio de rol
        user.user_type = serializer.validated_data["user_type"]
        user.save()

        # Registrar el cambio
        UserRoleChangeLog.objects.create(
            user=user,
            previous_role=previous_role,
            new_role=user.user_type,
            reason=serializer.validated_data["reason"],
            changed_by=request.user,
        )

        return Response(
            {
                "message": "Rol de usuario actualizado exitosamente",
                "user": UserProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


# Vista para cambiar la contraseña del usuario
@extend_schema(
    summary="Cambiar contraseña",
    description="Permite al usuario autenticado cambiar su contraseña actual por una nueva."
)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(
            {"message": "Contraseña actualizada exitosamente"},
            status=status.HTTP_200_OK,
        )
