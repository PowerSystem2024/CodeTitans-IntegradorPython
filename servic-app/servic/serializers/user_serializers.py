from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


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


# Cerrar sesión
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        required=True,
        error_messages={
            "required": "El token de actualización es obligatorio",
            "blank": "El token de actualización no puede estar vacío",
        },
    )


# Cambiar contraseña con el usuario autenticado
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={"required": "Debe ingresar su contraseña actual"},
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={"required": "Debe ingresar la nueva contraseña"},
    )
    new_password2 = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={"required": "Debe confirmar la nueva contraseña"},
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError(
                {"new_password2": "Las nuevas contraseñas no coinciden"}
            )
        from django.contrib.auth.password_validation import validate_password

        validate_password(attrs["new_password"], self.context["request"].user)
        return attrs


UserModel = (
    get_user_model()
)  # obtenemos el modelo de usuario actual para evitar problemas de importación circular


# Serializers para restablecimiento de contraseña
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, error_messages={"required": "El email es obligatorio"}
    )

    def validate_email(self, value):
        # No revelar si el email existe o no
        return value

    def get_user(self):
        email = self.validated_data["email"]
        try:
            return UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

    def save(self, **kwargs):
        user = self.get_user()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            return {"uid": uid, "token": token}
        return {"uid": None, "token": None}


# Serializers para confirmar el restablecimiento de contraseña
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={"required": "Debe ingresar la nueva contraseña"},
    )
    new_password2 = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={"required": "Debe confirmar la nueva contraseña"},
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError(
                {"new_password2": "Las nuevas contraseñas no coinciden"}
            )
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uid"]))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise serializers.ValidationError(
                {"uid": "El enlace de restablecimiento no es válido"}
            )
        if not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError(
                {"token": "El token de restablecimiento no es válido o ha expirado"}
            )
        from django.contrib.auth.password_validation import validate_password

        validate_password(attrs["new_password"], user)
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
