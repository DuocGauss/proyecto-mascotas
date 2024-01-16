from django.contrib import admin
from .models import Propietario, Cuidador, Servicio, Mascota, DetPrestacion

# Register your models here.
admin.site.register(Propietario)
admin.site.register(Cuidador)
admin.site.register(Servicio)
admin.site.register(Mascota)
admin.site.register(DetPrestacion)
