from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# si hacemos una comparacion con NodeJS, seria como el "server.js"
# la diferencia es que en NodeJS se usa el archivo "server.js" para definir la ruta de la API
# y en Django se usa el archivo "urls.py" para definir la ruta de la API
# el archivo "urls.py" es el encargado de manejar las peticiones y respuestas de la API

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("servic.urls")),
    # URLs de documentación de API
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Interfaces de UI opcionales:
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
