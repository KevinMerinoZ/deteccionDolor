from django.db import models

# Create your models here.
class IncidenciaExperimental(models.Model):
    idIncidencia = models.AutoField(primary_key=True)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=150)
    idSesionExperimental = models.ForeignKey("sesionExperimental.SesionExperimental", on_delete=models.CASCADE)
     
    is_active = models.BooleanField(default=True)
