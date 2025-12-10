from django.db import models

# Create your models here.
class Farmaco(models.Model):
    idfarmacos = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    presentacion = models.CharField(max_length=15)
    tipo_farmaco = models.CharField(max_length=25)
    via_administracion = models.CharField(max_length=15)
    consentracion = models.CharField(max_length=15)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre