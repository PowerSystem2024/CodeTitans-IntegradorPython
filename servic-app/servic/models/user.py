from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("common", "Usuario Común"),
        ("provider", "Prestador de Servicios"),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True
    )
    is_profile_complete = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class UserRoleChangeLog(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="role_changes"
    )
    previous_role = models.CharField(max_length=10, choices=User.USER_TYPE_CHOICES)
    new_role = models.CharField(max_length=10, choices=User.USER_TYPE_CHOICES)
    reason = models.TextField()
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="role_changes_made"
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de cambio de rol"
        verbose_name_plural = "Registros de cambios de rol"
        ordering = ["-changed_at"]

    def __str__(self):
        return f"Cambio de rol de {self.user.email} de {self.previous_role} a {self.new_role}"
