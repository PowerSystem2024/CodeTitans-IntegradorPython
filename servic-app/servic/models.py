from django.db import models

# Create your models here.

# Modelo de tabla para almacenar usuarios
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username