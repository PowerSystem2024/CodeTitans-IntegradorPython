from django.db import models
from .user import User
from .service import Service


class ServiceContract(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pendiente"),
        ("accepted", "Aceptado"),
        ("in_progress", "En Progreso"),
        ("completed", "Completado"),
        ("cancelled", "Cancelado"),
        ("rejected", "Rechazado"),
    )

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="contracts"
    )
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="client_contracts"
    )
    provider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="provider_contracts"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(
        help_text="Descripción detallada del trabajo a realizar"
    )
    location = models.CharField(
        max_length=200, help_text="Ubicación donde se realizará el servicio"
    )
    rejection_reason = models.TextField(
        null=True, blank=True, help_text="Motivo del rechazo si aplica"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    client_review = models.TextField(null=True, blank=True)
    provider_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    provider_review = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Contrato de Servicio"
        verbose_name_plural = "Contratos de Servicios"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Contrato de {self.service.title} - {self.client.email}"

    def save(self, *args, **kwargs):
        # Asegurar que el provider sea el propietario del servicio
        if self.provider != self.service.provider:
            raise ValueError("El prestador debe ser el propietario del servicio")
        super().save(*args, **kwargs)
