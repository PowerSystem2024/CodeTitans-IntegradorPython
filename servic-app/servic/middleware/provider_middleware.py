from django.http import JsonResponse
from rest_framework import status
from django.urls import resolve


class ServiceProviderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de URLs que requieren verificación de prestador
        provider_required_urls = [
            "provider-profile",
            # Agregar más URLs que requieran verificación de prestador
        ]

        # Obtener la URL actual
        current_url = resolve(request.path_info).url_name

        # Verificar si la URL actual requiere verificación de prestador
        if current_url in provider_required_urls:
            # Verificar si el usuario está autenticado
            if not request.user.is_authenticated:
                return JsonResponse(
                    {"detail": "Se requiere autenticación"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Verificar si el usuario es un prestador
            if request.user.user_type != "provider":
                return JsonResponse(
                    {
                        "detail": "Solo los prestadores de servicios pueden acceder a esta funcionalidad"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Verificar si el prestador tiene un perfil completo
            if not request.user.is_profile_complete:
                return JsonResponse(
                    {
                        "detail": "Debe completar su perfil de prestador antes de acceder a esta funcionalidad"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Verificar si el prestador está verificado
            try:
                if not request.user.provider_profile.is_verified:
                    return JsonResponse(
                        {
                            "detail": "Su perfil de prestador está pendiente de verificación"
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
            except:
                return JsonResponse(
                    {"detail": "No se encontró un perfil de prestador"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        response = self.get_response(request)
        return response
