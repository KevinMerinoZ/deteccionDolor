from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Cita(models.Model):
    ESTADO_ASIGNADA = 'Asignada'
    ESTADO_CANCELADA = 'Cancelada'
    ESTADO_FINALIZADA = 'Finalizada'

    ESTADOS = [
        (ESTADO_ASIGNADA, 'Asignar'),
        (ESTADO_CANCELADA, 'Cancelar'),
        (ESTADO_FINALIZADA, 'Finalizar'),
    ]
    idcitas = models.AutoField(primary_key=True)
    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()
    usuario = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE)
    protocolo_experimental = models.ForeignKey('protocoloExperimental.ProtocoloExperimental', on_delete=models.CASCADE)
    sala_laboratorio = models.ForeignKey('salaLaboratorio', on_delete=models.CASCADE)
    estado = models.CharField(max_length=15, choices=ESTADOS, default=ESTADO_ASIGNADA)

    is_active = models.BooleanField(default=True)

    def ya_paso(self):
        return timezone.now() >= self.fechaFin

    def __str__(self):
        return f"Cita {self.idcitas} - {self.usuario}"

class salaLaboratorio(models.Model):
    idSalaLaboratorio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, default=None)
    enUso = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre