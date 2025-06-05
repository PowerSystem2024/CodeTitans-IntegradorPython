from django.db import models
from .user import User


class ServiceProviderProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="provider_profile"
    )
    identification_type = models.CharField(
        max_length=20,
        choices=[
            ("dni", "DNI"),
            ("ce", "Carné de Extranjería"),
            ("passport", "Pasaporte"),
        ],
    )
    identification_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    certification_file = models.FileField(upload_to="certifications/")
    certification_description = models.TextField()
    years_of_experience = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Perfil de {self.user.email}"

    class Meta:
        verbose_name = "Perfil de Prestador"
        verbose_name_plural = "Perfiles de Prestadores"


class ProviderRequest(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pendiente"),
        ("approved", "Aprobada"),
        ("rejected", "Rechazada"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="provider_requests"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    request_reason = models.TextField(
        help_text="Razón por la que desea convertirse en prestador"
    )
    admin_response = models.TextField(
        blank=True, null=True, help_text="Respuesta del administrador"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="reviewed_requests"
    )

    class Meta:
        verbose_name = "Solicitud de Prestador"
        verbose_name_plural = "Solicitudes de Prestadores"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Solicitud de {self.user.email} - {self.get_status_display()}"
