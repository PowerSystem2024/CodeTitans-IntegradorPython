from django.urls import path
from ..views import UserProfileView, UserRoleChangeView

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path(
        "users/<int:user_id>/change-role/",
        UserRoleChangeView.as_view(),
        name="change-user-role",
    ),
]
