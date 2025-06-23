from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models import ServiceProviderProfile, Service, ProviderRequest
from ..serializers import (
    ServiceProviderProfileSerializer,
    ServiceSerializer,
    ServiceListSerializer,
)

User = get_user_model()


class AdminDashboardView(APIView):
    """Vista del dashboard administrativo con estadísticas"""

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        stats = {
            "total_users": User.objects.count(),
            "total_providers": User.objects.filter(user_type="provider").count(),
            "pending_provider_requests": ProviderRequest.objects.filter(
                status="pending"
            ).count(),
            "unverified_providers": ServiceProviderProfile.objects.filter(
                is_verified=False
            ).count(),
            "pending_services": Service.objects.filter(status="pending").count(),
            "active_services": Service.objects.filter(status="active").count(),
        }
        return Response(stats)


class AdminProviderListView(generics.ListAPIView):
    """Listar todos los prestadores para admin"""

    permission_classes = [permissions.IsAdminUser]
    serializer_class = ServiceProviderProfileSerializer

    def get_queryset(self):
        queryset = ServiceProviderProfile.objects.all()

        # Filtros opcionales
        is_verified = self.request.query_params.get("is_verified")
        if is_verified is not None:
            queryset = queryset.filter(is_verified=is_verified.lower() == "true")

        return queryset.order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        providers_data = []
        for profile in queryset:
            data = self.get_serializer(profile).data
            data["user_info"] = {
                "id": profile.user.id,
                "email": profile.user.email,
                "full_name": f"{profile.user.first_name} {profile.user.last_name}",
                "date_joined": profile.user.date_joined,
            }
            providers_data.append(data)

        return Response(providers_data)


class AdminProviderVerificationView(APIView):
    """Vista para que admins verifiquen/desverifiquen prestadores"""

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, user_id):
        """Ver información completa del prestador"""
        user = get_object_or_404(User, id=user_id, user_type="provider")

        try:
            profile = user.provider_profile
            serializer = ServiceProviderProfileSerializer(profile)
            return Response(
                {
                    "user_info": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": f"{user.first_name} {user.last_name}",
                        "user_type": user.user_type,
                        "date_joined": user.date_joined,
                        "is_profile_complete": user.is_profile_complete,
                    },
                    "profile": serializer.data,
                }
            )
        except ServiceProviderProfile.DoesNotExist:
            return Response(
                {"detail": "Este usuario no tiene un perfil de prestador"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, user_id):
        """Verificar/desverificar prestador"""
        user = get_object_or_404(User, id=user_id, user_type="provider")

        try:
            profile = user.provider_profile
        except ServiceProviderProfile.DoesNotExist:
            return Response(
                {"detail": "Este usuario no tiene un perfil de prestador"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validar datos recibidos
        is_verified = request.data.get("is_verified")
        admin_notes = request.data.get("admin_notes", "")

        if is_verified is None:
            return Response(
                {"detail": "Debe especificar el campo 'is_verified' (true/false)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Actualizar verificación
        profile.is_verified = bool(is_verified)
        if hasattr(profile, "admin_notes"):
            profile.admin_notes = admin_notes
        if hasattr(profile, "verified_by"):
            profile.verified_by = request.user if is_verified else None
        if hasattr(profile, "verified_at"):
            profile.verified_at = timezone.now() if is_verified else None
        profile.save()

        # Marcar perfil como completo
        user.is_profile_complete = True
        user.save()

        serializer = ServiceProviderProfileSerializer(profile)

        action = "verificado" if is_verified else "desverificado"
        return Response(
            {"message": f"Prestador {action} exitosamente", "profile": serializer.data}
        )


class AdminServiceListView(generics.ListAPIView):
    """Listar servicios para aprobación admin"""

    permission_classes = [permissions.IsAdminUser]
    serializer_class = ServiceListSerializer

    def get_queryset(self):
        queryset = Service.objects.all()

        # Filtros
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by("-created_at")


class AdminServiceApprovalView(APIView):
    """Aprobar/rechazar servicios"""

    permission_classes = [permissions.IsAdminUser]

    def put(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)

        new_status = request.data.get("status")
        admin_comment = request.data.get("admin_comment", "")

        if new_status not in ["active", "inactive", "pending"]:
            return Response(
                {"detail": "Status debe ser: active, inactive o pending"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service.status = new_status
        service.save()

        serializer = ServiceSerializer(service)

        return Response(
            {
                "message": f"Servicio {new_status} exitosamente",
                "service": serializer.data,
            }
        )
