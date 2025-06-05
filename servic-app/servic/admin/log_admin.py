from django.contrib import admin
from ..models import UserRoleChangeLog


# Configuración para el registro de cambios de rol
class UserRoleChangeLogAdmin(admin.ModelAdmin):
    list_display = ("user", "previous_role", "new_role", "changed_by", "changed_at")
    list_filter = ("previous_role", "new_role", "changed_at")
    search_fields = ("user__email", "reason")
    readonly_fields = ("changed_at",)
