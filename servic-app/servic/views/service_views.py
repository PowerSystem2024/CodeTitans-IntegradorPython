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


class ServiceCategoryListView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


class ServiceCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServiceCreateView(generics.CreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsProviderAndVerified]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)


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
