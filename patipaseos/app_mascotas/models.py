from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Propietario(AbstractUser):
    # Agregar un campo de rol
    es_cuidador = models.BooleanField(default=False)
    
    
class Cuidador(models.Model):
    propietario = models.OneToOneField(Propietario, on_delete=models.CASCADE)
    id_cuidador = models.AutoField(primary_key=True)
    especializacion = models.CharField(max_length=50)