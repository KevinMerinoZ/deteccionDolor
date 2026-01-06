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


