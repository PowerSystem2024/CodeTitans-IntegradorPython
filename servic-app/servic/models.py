from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# Modelo de tabla para almacenar usuarios
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('common', 'Usuario Común'),
        ('provider', 'Prestador de Servicios'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)
    is_profile_complete = models.BooleanField(default=False)
    
    # Usar email como campo de autenticación
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email