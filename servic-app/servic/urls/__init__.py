from django.urls import path, include

urlpatterns = [
    path("", include("servic.urls.auth_urls")),
    path("", include("servic.urls.user_urls")),
    path("", include("servic.urls.provider_urls")),
    path("", include("servic.urls.service_urls")),
    path("", include("servic.urls.admin_urls")),
    path("", include("servic.urls.contract_urls")),
]
