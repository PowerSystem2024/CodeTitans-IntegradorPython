from django.urls import path
from ..views import (
    ServiceProviderProfileView,
    ProviderRequestView,
    ProviderRequestListView,
    ProviderRequestDetailView,
)

urlpatterns = [
    path(
        "provider/profile/",
        ServiceProviderProfileView.as_view(),
        name="provider-profile",
    ),
    path(
        "provider/request/",
        ProviderRequestView.as_view(),
        name="create-provider-request",
    ),
    path(
        "provider/requests/",
        ProviderRequestListView.as_view(),
        name="list-provider-requests",
    ),
    path(
        "provider/requests/<int:pk>/",
        ProviderRequestDetailView.as_view(),
        name="review-provider-request",
    ),
]
