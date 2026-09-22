from django.db import models
from django.utils import timezone
from datetime import date, time, datetime

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
    def get_hora_act():
        return timezone.now().time()

    def get_hora_act():
        return (timezone.now() + timezone.timedelta(hora=1)).time()
    
    idcitas = models.AutoField(primary_key=True)
    fecha = models.DateField(default=timezone.now)
    horaInicio = models.TimeField(default=get_hora_act)
    horaFin = models.TimeField(default=get_hora_act)
    usuario = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE)
    protocolo_experimental = models.ForeignKey('protocoloExperimental.ProtocoloExperimental', on_delete=models.CASCADE)
    sala_laboratorio = models.ForeignKey('cita.salaLaboratorio', on_delete=models.CASCADE)
    estado = models.CharField(max_length=15, choices=ESTADOS, default=ESTADO_ASIGNADA)

    is_active = models.BooleanField(default=True)

    def ya_paso(self):
        if timezone.now().date() >= self.fecha and timezone.now().time() > self.horaFin:
            return True
        return False

    def fecha_horaInicio(self):
        return timezone.make_aware(datetime.combine(self.fecha, self.horaInicio))

    def fecha_horaFin(self):
        return timezone.make_aware(datetime.combine(self.fecha, self.horaFin))

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