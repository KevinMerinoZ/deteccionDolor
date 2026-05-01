from django.db import models

# Create your models here.
class ActividadUsuario(models.Model):
    idActividad = models.AutoField(primary_key=True)
    usuario = models.ForeignKey("usuario.Usuario", on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    ultimaActividad = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    direccionIP = models.GenericIPAddressField()
    
    def __str__(self):
        return f"Actividad de {self.usuario.nombre} iniciada el {self.fechaInicio}"
    