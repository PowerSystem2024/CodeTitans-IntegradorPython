from rest_framework import permissions
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class IsProviderAndVerified(permissions.BasePermission):
    """
    Permiso personalizado para permitir el acceso solo a usuarios que son prestadores
    de servicios y tienen su perfil verificado.
    """

    message = _(
        "Solo los prestadores de servicios con un perfil verificado pueden acceder a esta funcionalidad."
    )

    def has_permission(self, request, view):
        # Asumiendo que IsAuthenticated ya ha sido verificado en permission_classes
        # Esto significa que request.user no es AnonymousUser aquí.

        if not request.user.is_authenticated:
            # Esto no debería ocurrir si IsAuthenticated está antes, pero como fallback.
            return False

        if request.user.user_type != "provider":
            raise APIException(
                detail=_(
                    "Solo los prestadores de servicios pueden acceder a esta funcionalidad."
                ),
                code=403,
            )

        if not hasattr(request.user, "provider_profile"):
            raise APIException(
                detail=_(
                    "No se encontró un perfil de prestador asociado a este usuario."
                ),
                code=404,
            )

        if not request.user.provider_profile.is_verified:
            raise APIException(
                detail=_("Su perfil de prestador está pendiente de verificación."),
                code=403,
            )

        # Si tiene un perfil y no está completo
        if not request.user.is_profile_complete:
            raise APIException(
                detail=_(
                    "Debe completar su perfil de prestador antes de acceder a esta funcionalidad."
                ),
                code=403,
            )

        return True
