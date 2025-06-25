from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from ..models import ServiceProviderProfile, ProviderRequest
from ..serializers import (
    ServiceProviderProfileSerializer,
    ProviderRequestSerializer,
    ProviderRequestCreateSerializer,
    ProviderRequestReviewSerializer,
)
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Obtener o crear perfil de proveedor",
    description="Permite consultar (GET), crear (POST) o actualizar (PUT) el perfil del proveedor autenticado."
)

class ServiceProviderProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)


    @extend_schema(
        summary="Obtener perfil de proveedor",
        description="Devuelve los datos del perfil del proveedor autenticado."
    )
    def get(self, request, *args, **kwargs):
        try:
            profile = request.user.provider_profile
        except ServiceProviderProfile.DoesNotExist:
            return Response(
                {"detail": "No se encontró un perfil de prestador de servicios"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ServiceProviderProfileSerializer(profile)
        return Response(serializer.data)

    @extend_schema(
        summary="Crear perfil de proveedor",
        description="Permite a un usuario con rol 'provider' crear su perfil de proveedor. Requiere archivo de certificación."
    )

    def post(self, request, *args, **kwargs):
        # Prints de depuración
        print("FILES:", request.FILES)
        print("DATA:", request.data)
        # Solo prestadores pueden crear perfil
        if request.user.user_type != "provider":
            return Response(
                {"detail": "Solo los prestadores de servicios pueden crear un perfil"},
                status=status.HTTP_403_FORBIDDEN,
            )
        # No permitir crear más de un perfil
        if hasattr(request.user, "provider_profile"):
            return Response(
                {"detail": "Ya existe un perfil de prestador de servicios"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Verificar que se haya enviado el archivo
        if "certification_file" not in request.FILES:
            return Response(
                {"certification_file": ["El archivo de certificación es obligatorio"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ServiceProviderProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            request.user.is_profile_complete = True
            request.user.save()
            return Response(
                {"message": "Perfil creado exitosamente", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Actualizar perfil de proveedor",
        description="Permite actualizar los datos del perfil del proveedor autenticado. Se pueden enviar solo los campos a modificar."
    )

    def put(self, request, *args, **kwargs):
        try:
            profile = request.user.provider_profile
        except ServiceProviderProfile.DoesNotExist:
            return Response(
                {"detail": "No se encontró un perfil de prestador de servicios"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ServiceProviderProfileSerializer(
            profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Perfil actualizado exitosamente", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Solicitar ser proveedor",
    description="Permite a un usuario solicitar convertirse en proveedor de servicios."
)

class ProviderRequestView(generics.CreateAPIView):
    serializer_class = ProviderRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(
    summary="Listar solicitudes de proveedor",
    description="Permite a un administrador ver todas las solicitudes para convertirse en proveedor. Se puede filtrar por estado."
)

class ProviderRequestListView(generics.ListAPIView):
    serializer_class = ProviderRequestSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        status_filter = self.request.query_params.get("status", None)
        queryset = ProviderRequest.objects.all()

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

@extend_schema(
    summary="Detalle y revisión de solicitud de proveedor",
    description="Permite a un administrador ver el detalle y aprobar o rechazar una solicitud de proveedor."
)

class ProviderRequestDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProviderRequestReviewSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ProviderRequest.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Si la solicitud es aprobada, cambiar el rol del usuario
        if serializer.validated_data.get("status") == "approved":
            user = instance.user
            user.user_type = "provider"
            user.save()

        # Guardar la respuesta del administrador
        serializer.save(reviewed_by=request.user)

        return Response(
            {
                "message": "Solicitud actualizada exitosamente",
                "request": ProviderRequestSerializer(instance).data,
            }
        )
