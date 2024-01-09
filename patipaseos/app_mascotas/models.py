from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Propietario(AbstractUser):
    # Agregar un campo de rol
    es_cuidador = models.BooleanField(default=False)