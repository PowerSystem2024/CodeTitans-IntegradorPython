from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q  # para filtrar por cliente o prestador

# from ..models import ServiceContract
from servic.models.contract import ServiceContract

from ..serializers.contract_serializers import (
    ServiceContractCreateSerializer,
    ServiceContractSerializer,
    ServiceContractUpdateSerializer,
    ServiceContractReviewSerializer,
    ServiceContractRejectSerializer,
)


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


class ServiceContractListView(generics.ListAPIView):
    serializer_class = ServiceContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ServiceContract.objects.filter(Q(client=user) | Q(provider=user))


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


# para que el prestador pueda aceptar solicitudes
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


# para que el prestador pueda rechazar solicitudes con un motivo
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
