from rest_framework import serializers
from ..models import ServiceContract, Service
from django.utils import timezone


class ServiceContractCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceContract
        fields = ["service", "start_date", "description", "location"]
        read_only_fields = ["provider", "client"]

    def validate(self, attrs):
        service = attrs["service"]
        start_date = attrs["start_date"]

        # Validar que el servicio esté activo
        if service.status != "active":
            raise serializers.ValidationError("El servicio no está disponible")

        # Validar que la fecha de inicio sea futura
        if start_date <= timezone.now():
            raise serializers.ValidationError("La fecha de inicio debe ser futura")

        # Validar que la fecha esté dentro de los días disponibles del servicio
        service_days = [day.strip() for day in service.available_days.split(",")]

        # Mapeo de nombres de días de la semana de inglés a español
        day_name_map = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo",
        }

        # Obtener el nombre del día en inglés y convertirlo a español
        start_day_english = start_date.strftime("%A")
        start_day_spanish = day_name_map.get(
            start_day_english, start_day_english
        )  # Fallback to english if not found

        if start_day_spanish not in service_days:
            raise serializers.ValidationError(
                "La fecha seleccionada no está disponible"
            )

        # Validar que la hora esté dentro del horario disponible
        start_time = start_date.time()
        if not (service.availability_start <= start_time <= service.availability_end):
            raise serializers.ValidationError("La hora seleccionada no está disponible")

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        service = validated_data["service"]

        # Establecer el cliente
        validated_data["client"] = request.user
        # Establecer el proveedor
        validated_data["provider"] = service.provider

        return super().create(validated_data)


class ServiceContractSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source="service.title", read_only=True)
    client_name = serializers.SerializerMethodField(read_only=True)
    provider_name = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = ServiceContract
        fields = [
            "id",
            "service",
            "service_title",
            "client",
            "client_name",
            "provider",
            "provider_name",
            "status",
            "status_display",
            "start_date",
            "end_date",
            "description",
            "location",
            "rejection_reason",
            "client_rating",
            "client_review",
            "provider_rating",
            "provider_review",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_client_name(self, obj):
        return f"{obj.client.first_name} {obj.client.last_name}"

    def get_provider_name(self, obj):
        return f"{obj.provider.first_name} {obj.provider.last_name}"


class ServiceContractUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceContract
        fields = ["status", "end_date"]

    def validate(self, attrs):
        if attrs.get("status") == "completed" and not attrs.get("end_date"):
            raise serializers.ValidationError(
                "La fecha de finalización es requerida para completar el servicio"
            )
        return attrs


class ServiceContractReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceContract
        fields = [
            "client_rating",
            "client_review",
            "provider_rating",
            "provider_review",
        ]

    def validate(self, attrs):
        if not self.instance.status == "completed":
            raise serializers.ValidationError(
                "Solo se pueden calificar servicios completados"
            )
        return attrs


class ServiceContractRejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceContract
        fields = ["rejection_reason"]

    def validate(self, attrs):
        if not attrs.get("rejection_reason"):
            raise serializers.ValidationError(
                "Debe proporcionar un motivo para rechazar la solicitud"
            )
        return attrs
