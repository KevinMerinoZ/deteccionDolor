from django.db import models
from django.utils import timezone

# Create your models here.
class Farmaco(models.Model):
    idfarmacos = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    presentacion = models.CharField(max_length=15)
    tipo_farmaco = models.CharField(max_length=25)
    fecha_llegada = models.DateField()
    fecha_abierto = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre