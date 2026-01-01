from django.db import models

# Create your models here.
class Cita(models.Model):
    idcitas = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    usuario = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE)
    protocolo_experimental = models.ForeignKey('protocoloExperimental.ProtocoloExperimental', on_delete=models.CASCADE)
    estado = models.CharField(max_length=45)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cita {self.idcitas} - {self.usuario}"