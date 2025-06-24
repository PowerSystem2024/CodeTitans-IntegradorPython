from django.contrib import admin
from ..models import (
    User,
    ServiceProviderProfile,
    ProviderRequest,
    UserRoleChangeLog,
    ServiceCategory,
    Service,
    ServiceImage,
    ServiceContract,
)
from .user_admin import CustomUserAdmin
from .provider_admin import ServiceProviderProfileAdmin, ProviderRequestAdmin
from .log_admin import UserRoleChangeLogAdmin

# Registro de modelos en el panel de administración
admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceProviderProfile, ServiceProviderProfileAdmin)
admin.site.register(ProviderRequest, ProviderRequestAdmin)
admin.site.register(UserRoleChangeLog, UserRoleChangeLogAdmin)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(ServiceImage)
admin.site.register(ServiceContract)

# Configuración del panel de administración
admin.site.site_header = "Servic Admin"
admin.site.site_title = "Servic Admin Portal"
admin.site.index_title = "Bienvenido al panel de administración de Servic"
# admin.site.site_url = None  # Deshabilitar el enlace al sitio principal
admin.site.site_url = "https://github.com/PowerSystem2024/CodeTitans-IntegradorPython"

admin.site.empty_value_display = (
    "-sin datos-"  # Valor por defecto para campos vacíos en el admin
)

# Templates personalizados.
# admin.site.login_template = "admin/login.html"

# Mensaje personalizado de despedida
# admin.site.logout_template = "admin/logout.html"
