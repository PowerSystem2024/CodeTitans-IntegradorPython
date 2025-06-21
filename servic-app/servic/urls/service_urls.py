from django.urls import path
from ..views import (
    ServiceCategoryListView,
    ServiceCategoryDetailView,
    ServiceCreateView,
    ServiceListView,
    ServiceDetailView,
    ServiceImageUploadView,
    ServiceImageDeleteView,
    ServiceImageSetPrimaryView,
)

urlpatterns = [
    # URLs para categorías de servicios
    path(
        "categories/", ServiceCategoryListView.as_view(), name="service-category-list"
    ),  # listar todas las categorias que existen
    path(
        "categories/<int:pk>/",
        ServiceCategoryDetailView.as_view(),
        name="service-category-detail",
    ),  # obtener una categoria en especifico
    # URLs para servicios
    path(
        "services/", ServiceListView.as_view(), name="service-list"
    ),  # listar todos los servicios
    path(
        "services/create/", ServiceCreateView.as_view(), name="service-create"
    ),  # crear un servicio
    path(
        "services/<int:pk>/", ServiceDetailView.as_view(), name="service-detail"
    ),  # obtener un servicio en especifico
    # URLs para imágenes de servicios
    path(
        "services/<int:service_id>/images/",
        ServiceImageUploadView.as_view(),
        name="service-image-upload",
    ),  # subir imagenes a un servicio
    path(
        "services/images/<int:pk>/",
        ServiceImageDeleteView.as_view(),
        name="service-image-delete",
    ),  # eliminar una imagen de un servicio
    path(
        "services/images/<int:pk>/set-primary/",
        ServiceImageSetPrimaryView.as_view(),
        name="service-image-set-primary",
    ),  # establecer una imagen como principal de un servicio
]
