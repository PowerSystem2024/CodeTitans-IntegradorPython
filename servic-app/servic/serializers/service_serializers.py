from rest_framework import serializers
from ..models import ServiceCategory, Service, ServiceImage
from django.core.validators import MinValueValidator
from django.utils import timezone


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name", "description", "icon", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ["id", "image", "is_primary"]
        read_only_fields = ["id"]

    def validate_image(self, value):
        # Validar tamaño máximo (5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("La imagen no debe superar los 5MB")

        # Validar tipo de archivo
        allowed_types = ["image/jpeg", "image/png", "image/jpg"]
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Solo se permiten imágenes en formato JPEG o PNG"
            )

        return value


class ServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, required=False)
    provider_email = serializers.EmailField(source="provider.email", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    price_type_display = serializers.CharField(
        source="get_price_type_display", read_only=True
    )

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_name",
            "provider",
            "provider_email",
            "price",
            "price_type",
            "price_type_display",
            "location",
            "city",
            "state",
            "country",
            "availability_start",
            "availability_end",
            "available_days",
            "status",
            "status_display",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "provider", "created_at", "updated_at"]

    def validate(self, attrs):
        # Validar que el prestador esté verificado
        provider = self.context["request"].user
        if not provider.provider_profile.is_verified:
            raise serializers.ValidationError(
                "Debe tener un perfil de prestador verificado para publicar servicios"
            )

        # Validar horarios de disponibilidad
        if attrs.get("availability_start") and attrs.get("availability_end"):
            if attrs["availability_start"] >= attrs["availability_end"]:
                raise serializers.ValidationError(
                    "La hora de inicio debe ser anterior a la hora de fin"
                )

        # Validar días disponibles
        if attrs.get("available_days"):
            valid_days = [
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
                "Domingo",
            ]
            days = [day.strip() for day in attrs["available_days"].split(",")]
            if not all(day in valid_days for day in days):
                raise serializers.ValidationError(
                    "Los días disponibles deben ser válidos (Lunes, Martes, etc.)"
                )

        return attrs

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0")
        return value

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        service = Service.objects.create(**validated_data)

        # Crear imágenes asociadas
        for image_data in images_data:
            ServiceImage.objects.create(service=service, **image_data)

        return service

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images", None)

        # Actualizar campos del servicio
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar imágenes si se proporcionan
        if images_data is not None:
            # Eliminar imágenes existentes
            instance.images.all().delete()
            # Crear nuevas imágenes
            for image_data in images_data:
                ServiceImage.objects.create(service=instance, **image_data)

        return instance


class ServiceListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    provider_name = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "category_name",
            "provider_name",
            "price",
            "price_type",
            "location",
            "primary_image",
            "status",
            "created_at",
        ]

    def get_provider_name(self, obj):
        return f"{obj.provider.first_name} {obj.provider.last_name}"

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        return None
