from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q  # para filtrar por cliente o prestador
from servic.models.contract import ServiceContract
from ..serializers.contract_serializers import (
    ServiceContractCreateSerializer,
    ServiceContractSerializer,
    ServiceContractUpdateSerializer,
    ServiceContractReviewSerializer,
    ServiceContractRejectSerializer,
)
from drf_spectacular.utils import extend_schema


# Decorador para documentar las vistas de la API
@extend_schema(
    summary="Crear contrato de servicio",
    description="Permite a un cliente crear un contrato de servicio con un proveedor.",
)
# Crear un contrato de servicio
class ServiceContractCreateView(generics.CreateAPIView):
    serializer_class = ServiceContractCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Serializar el objeto creado con el serializador completo
        full_serializer = ServiceContractSerializer(serializer.instance)
        return Response(
            full_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


@extend_schema(
    summary="Listar contratos de servicio",
    description="Lista todos los contratos donde el usuario es cliente o proveedor.",
)
# Listar contratos de servicio
class ServiceContractListView(generics.ListAPIView):
    serializer_class = ServiceContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ServiceContract.objects.filter(Q(client=user) | Q(provider=user))


@extend_schema(
    summary="Detalle y actualización de contrato de servicio",
    description="Permite ver o actualizar un contrato de servicio.",
)
# Detalle y actualización de contrato de servicio
class ServiceContractDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ServiceContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ServiceContract.objects.filter(Q(client=user) | Q(provider=user))

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ServiceContractUpdateSerializer
        return ServiceContractSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(ServiceContractSerializer(instance).data)


@extend_schema(
    summary="Revisar contrato de servicio",
    description="Permite a las partes dejar una reseña sobre el contrato.",
)
# Revisar contrato de servicio
class ServiceContractReviewView(generics.UpdateAPIView):
    serializer_class = ServiceContractReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ServiceContract.objects.filter(Q(client=user) | Q(provider=user))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(ServiceContractSerializer(instance).data)


@extend_schema(
    summary="Aceptar contrato de servicio",
    description="Permite al proveedor aceptar una solicitud de contrato.",
)
# Aceptar contrato de servicio
class ServiceContractAcceptView(generics.UpdateAPIView):
    serializer_class = ServiceContractUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceContract.objects.filter(
            provider=self.request.user, status="pending"
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "accepted"
        instance.save()
        return Response(ServiceContractSerializer(instance).data)


@extend_schema(
    summary="Rechazar contrato de servicio",
    description="Permite al proveedor rechazar una solicitud de contrato con motivo.",
)
# prestador puede rechazar solicitudes con un motivo
class ServiceContractRejectView(generics.UpdateAPIView):
    serializer_class = ServiceContractRejectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceContract.objects.filter(
            provider=self.request.user, status="pending"
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.status = "rejected"
        instance.rejection_reason = serializer.validated_data["rejection_reason"]
        instance.save()
        return Response(ServiceContractSerializer(instance).data)
