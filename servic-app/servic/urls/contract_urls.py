from django.urls import path
from ..views.contract_views import (
    ServiceContractCreateView,
    ServiceContractListView,
    ServiceContractDetailView,
    ServiceContractReviewView,
    ServiceContractAcceptView,
    ServiceContractRejectView,
)

urlpatterns = [
    path(
        "contracts/create/", ServiceContractCreateView.as_view(), name="create-contract"
    ),
    path("contracts/", ServiceContractListView.as_view(), name="list-contracts"),
    path(
        "contracts/<int:pk>/",
        ServiceContractDetailView.as_view(),
        name="contract-detail",
    ),
    path(
        "contracts/<int:pk>/review/",
        ServiceContractReviewView.as_view(),
        name="contract-review",
    ),
    path(
        "contracts/<int:pk>/accept/",
        ServiceContractAcceptView.as_view(),
        name="contract-accept",
    ),
    path(
        "contracts/<int:pk>/reject/",
        ServiceContractRejectView.as_view(),
        name="contract-reject",
    ),
]
