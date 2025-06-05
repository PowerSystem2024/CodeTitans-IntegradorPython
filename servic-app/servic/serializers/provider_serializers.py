from rest_framework import serializers
from ..models import ServiceProviderProfile, ProviderRequest


class ServiceProviderProfileSerializer(serializers.ModelSerializer):
    certification_file = serializers.FileField(
        required=True,
        error_messages={
            "required": "El archivo de certificación es obligatorio",
            "invalid": "El archivo de certificación no es válido",
        },
    )

    class Meta:
        model = ServiceProviderProfile
        fields = [
            "id",
            "identification_type",
            "identification_number",
            "phone_number",
            "address",
            "city",
            "state",
            "country",
            "certification_file",
            "certification_description",
            "years_of_experience",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_verified", "created_at", "updated_at"]

    def validate_certification_file(self, value):
        allowed_types = ["image/jpeg", "image/png", "application/pdf"]
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "El archivo debe ser una imagen (JPEG, PNG) o un PDF"
            )

        if value.size > 5 * 1024 * 1024:  # 5MB en bytes
            raise serializers.ValidationError("El archivo no debe superar los 5MB")
        return value

    def validate_identification_number(self, value):
        if ServiceProviderProfile.objects.filter(identification_number=value).exists():
            raise serializers.ValidationError(
                "Este número de identificación ya está registrado"
            )
        return value

    def validate_phone_number(self, value):
        if not value.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise serializers.ValidationError(
                "El número de teléfono debe contener solo dígitos, espacios, guiones y el símbolo +"
            )
        return value


class ProviderRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = ProviderRequest
        fields = [
            "id",
            "user_email",
            "user_name",
            "status",
            "status_display",
            "request_reason",
            "admin_response",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "admin_response", "created_at", "updated_at"]

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class ProviderRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderRequest
        fields = ["request_reason"]

    def validate(self, attrs):
        user = self.context["request"].user

        if user.user_type == "provider":
            raise serializers.ValidationError("Ya eres un prestador de servicios")

        if ProviderRequest.objects.filter(user=user, status="pending").exists():
            raise serializers.ValidationError("Ya tienes una solicitud pendiente")

        return attrs


class ProviderRequestReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderRequest
        fields = ["status", "admin_response"]

    def validate(self, attrs):
        if attrs["status"] == "rejected" and not attrs.get("admin_response"):
            raise serializers.ValidationError(
                {"admin_response": "Debe proporcionar una razón para el rechazo"}
            )
        return attrs
