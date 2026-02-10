from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone

class Checada(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    fecha = models.DateField(default=timezone.now)
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'fecha')

    def __str__(self):
        return f"{self.usuario} - {self.fecha}"
    def horas_trabajadas(self):
        if self.hora_entrada and self.hora_salida:
            delta = self.hora_salida - self.hora_entrada
            total_seconds = int(delta.total_seconds())
            horas = total_seconds // 3600
            minutos = (total_seconds % 3600) // 60
            return f"{horas:02d}:{minutos:02d}"
        return "-"
