from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        error_messages={"required": "La contraseña es obligatoria"},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={"required": "La contraseña no coincide"},
    )
    first_name = serializers.CharField(
        required=True, error_messages={"required": "El nombre es obligatorio"}
    )
    last_name = serializers.CharField(
        required=True, error_messages={"required": "El apellido es obligatorio"}
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "El email es obligatorio",
            "invalid": "El email no es valido",
            "unique": "El email ya esta registrado",
        },
    )

    class Meta:
        model = User
        fields = ("email", "password", "password2", "first_name", "last_name")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Las contraseñas no coinciden"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        if "username" not in validated_data:
            validated_data["username"] = validated_data["email"].split("@")[0]
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "username": self.user.username,
            "user_type": self.user.user_type,
        }
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "user_type")
        read_only_fields = ("email", "user_type")


class UserRoleChangeSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        error_messages={
            "invalid_choice": 'El tipo de usuario debe ser "common" o "provider"'
        },
    )
    reason = serializers.CharField(
        required=True,
        max_length=500,
        error_messages={
            "required": "Debe proporcionar una razón para el cambio de rol",
            "max_length": "La razón no puede exceder los 500 caracteres",
        },
    )

    class Meta:
        model = User
        fields = ("user_type", "reason")
        read_only_fields = ("id",)

    def validate(self, attrs):
        user = self.instance
        new_role = attrs["user_type"]

        if user.user_type == new_role:
            raise serializers.ValidationError(
                {"user_type": "El usuario ya tiene asignado este rol"}
            )

        if user.is_superuser:
            raise serializers.ValidationError(
                {"user_type": "No se puede cambiar el rol de un superusuario"}
            )

        return attrs
