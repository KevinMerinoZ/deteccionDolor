from django.db import models
from django.contrib.auth.models import User

# app_detectordolor/models.py
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')

    idUsuarios = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=55)
    apellido_paterno = models.CharField(max_length=45)
    apellido_materno = models.CharField(max_length=45, null=True, blank=True)
    correo = models.EmailField(max_length=55)
    fecha_registro = models.DateField()

    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

class SesionExperimental(models.Model):
    idsesionExperimental = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nombre_experimento = models.CharField(max_length=45)
    observaciones = models.CharField(max_length=45)
    numero_mediciones = models.IntegerField()
    farmaco = models.ForeignKey("farmaco.Farmaco", on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    protocolo_experimental = models.ForeignKey('protocoloExperimental.ProtocoloExperimental', on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_experimento


class ResultadoMedicion(models.Model):
    idresultadoMedicion = models.AutoField(primary_key=True)
    medicion_obtenida = models.CharField(max_length=20)
    numero_medicion = models.IntegerField()
    sesion_experimental = models.ForeignKey(SesionExperimental, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Medición {self.numero_medicion} ({self.sesion_experimental})"

