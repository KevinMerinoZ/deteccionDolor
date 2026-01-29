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
    fecha = models.DateField()
    hora = models.TimeField()
    usuario = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE)
    protocolo_experimental = models.ForeignKey('protocoloExperimental.ProtocoloExperimental', on_delete=models.CASCADE)
    estado = models.CharField(max_length=15, choices=ESTADOS, default=ESTADO_ASIGNADA)

    is_active = models.BooleanField(default=True)

    def ya_paso(self):
        fecha_hora = timezone.make_aware(
            datetime.datetime.combine(self.fecha, self.hora)
        )
        return timezone.now() >= fecha_hora

    def __str__(self):
        return f"Cita {self.idcitas} - {self.usuario}"