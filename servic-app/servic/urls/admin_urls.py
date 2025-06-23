from django.urls import path
from ..views import (
    AdminProviderVerificationView,
    AdminProviderListView,
    AdminServiceApprovalView,
    AdminServiceListView,
    AdminDashboardView,
)

urlpatterns = [
    # Panel de administración (estadisticas)
    path(
        "admin/dashboard/",
        AdminDashboardView.as_view(),
        name="admin-dashboard",
    ),
    # Gestión de prestadores por admin (listado, verificación, etc)
    path(
        "admin/providers/",
        AdminProviderListView.as_view(),
        name="admin-provider-list",
    ),
    # Verificación de prestadores por admin
    path(
        "admin/providers/<int:user_id>/verify/",
        AdminProviderVerificationView.as_view(),
        name="admin-verify-provider",
    ),
    # Gestión de servicios por admin (listado, aprobación, etc)
    path(
        "admin/services/",
        AdminServiceListView.as_view(),
        name="admin-service-list",
    ),
    # Aprobar/rechazar servicios por admin
    path(
        "admin/services/<int:service_id>/approve/",
        AdminServiceApprovalView.as_view(),
        name="admin-approve-service",
    ),
]
