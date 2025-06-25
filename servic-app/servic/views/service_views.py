from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from ..models import ServiceCategory, Service, ServiceImage
from ..serializers import (
    ServiceCategorySerializer,
    ServiceSerializer,
    ServiceListSerializer,
    ServiceImageSerializer,
)
from ..permissions import IsProviderAndVerified
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Listar y crear categorías de servicio",
    description="Permite listar todas las categorías de servicio o crear una nueva (solo para usuarios autenticados)."
)

class ServiceCategoryListView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]

@extend_schema(
    summary="Detalle, actualización y eliminación de categoría de servicio",
    description="Permite ver, actualizar o eliminar una categoría de servicio."
)

class ServiceCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@extend_schema(
    summary="Crear un servicio",
    description="Permite a un proveedor crear un nuevo servicio."
)

class ServiceCreateView(generics.CreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsProviderAndVerified]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

@extend_schema(
    summary="Listar servicios",
    description="Permite listar todos los servicios activos con filtros y búsqueda."
)

class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "status", "price_type", "city", "state", "country"]
    search_fields = ["title", "description", "location"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Service.objects.filter(status="active")

        # Filtrar por rango de precio
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Filtrar por disponibilidad
        available_day = self.request.query_params.get("available_day")
        if available_day:
            queryset = queryset.filter(available_days__icontains=available_day)

        return queryset

@extend_schema(
    summary="Detalle, actualización y eliminación de servicio",
    description="Permite ver, actualizar o eliminar un servicio específico."
)

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return Service.objects.all()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def check_object_permissions(self, request, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if obj.provider != request.user and not request.user.is_staff:
                self.permission_denied(
                    request,
                    message="Solo el propietario del servicio puede modificarlo",
                )
        return super().check_object_permissions(request, obj)

@extend_schema(
    summary="Subir imagen de servicio",
    description="Permite a un proveedor subir una imagen para uno de sus servicios. Si es la primera imagen, se marca como principal."
)

class ServiceImageUploadView(generics.CreateAPIView):
    serializer_class = ServiceImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return ServiceImage.objects.filter(service__provider=self.request.user)

    def perform_create(self, serializer):
        service_id = self.kwargs.get("service_id")
        service = get_object_or_404(Service, id=service_id, provider=self.request.user)

        # Si es la primera imagen, marcarla como principal
        if not service.images.exists():
            serializer.save(service=service, is_primary=True)
        else:
            serializer.save(service=service)

@extend_schema(
    summary="Eliminar imagen de servicio",
    description="Permite a un proveedor eliminar una imagen de uno de sus servicios. Si la imagen era principal, otra imagen será marcada como principal."
)

class ServiceImageDeleteView(generics.DestroyAPIView):
    serializer_class = ServiceImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceImage.objects.filter(service__provider=self.request.user)

    def perform_destroy(self, instance):
        # Si es la imagen principal, marcar otra como principal
        if instance.is_primary:
            next_image = self.get_queryset().exclude(id=instance.id).first()
            if next_image:
                next_image.is_primary = True
                next_image.save()
        instance.delete()

@extend_schema(
    summary="Marcar imagen como principal",
    description="Permite a un proveedor marcar una imagen específica como la principal de su servicio."
)

class ServiceImageSetPrimaryView(generics.UpdateAPIView):
    serializer_class = ServiceImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceImage.objects.filter(service__provider=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Desmarcar todas las imágenes como principales
        self.get_queryset().filter(service=instance.service).update(is_primary=False)

        # Marcar la imagen seleccionada como principal
        instance.is_primary = True
        instance.save()

        return Response(self.get_serializer(instance).data)
