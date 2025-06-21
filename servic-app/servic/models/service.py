from django.db import models
from .user import User


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to="category_icons/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría de Servicio"
        verbose_name_plural = "Categorías de Servicios"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Service(models.Model):
    STATUS_CHOICES = (
        ("active", "Activo"),
        ("inactive", "Inactivo"),
        ("pending", "Pendiente"),
    )

    PRICE_TYPE_CHOICES = (
        ("hourly", "Por Hora"),
        ("fixed", "Precio Fijo"),
        ("negotiable", "Negociable"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name="services"
    )
    provider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="services"
    )

    # Precio y tipo de precio
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES)

    # Ubicación
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    # Disponibilidad
    availability_start = models.TimeField()
    availability_end = models.TimeField()
    available_days = models.CharField(
        max_length=100
    )  # Ejemplo: "Lunes,Martes,Miércoles"

    # Estado y fechas
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.provider.email}"


class ServiceImage(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="service_images/")
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de Servicio"
        verbose_name_plural = "Imágenes de Servicios"
        ordering = ["-is_primary", "-created_at"]

    def __str__(self):
        return f"Imagen de {self.service.title}"