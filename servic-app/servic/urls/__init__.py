from django.urls import path, include

urlpatterns = [
    path("", include("servic.urls.auth_urls")),
    path("", include("servic.urls.user_urls")),
    path("", include("servic.urls.provider_urls")),
]
