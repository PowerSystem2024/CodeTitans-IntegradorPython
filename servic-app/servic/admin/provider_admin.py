from django.contrib import admin
from ..models import ServiceProviderProfile, ProviderRequest


# Configuración para el perfil de prestador
class ServiceProviderProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "identification_type",
        "identification_number",
        "phone_number",
        "is_verified",
        "created_at",
    )
    list_filter = ("is_verified", "identification_type", "created_at")
    search_fields = ("user__email", "identification_number", "phone_number")
    readonly_fields = ("created_at", "updated_at")


# Configuración para las solicitudes de prestador
class ProviderRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "created_at", "updated_at", "reviewed_by")
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "request_reason", "admin_response")
    readonly_fields = ("created_at", "updated_at")
