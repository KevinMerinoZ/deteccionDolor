from django.db import models


class SustanciaExperimental(models.Model):
    idsustanciaExperimental = models.AutoField(primary_key=True)
    nombre_sustancia = models.CharField(max_length=45)
    tipo = models.CharField(max_length=25)
    consentracion = models.CharField(max_length=15, default='')
    presentacion = models.CharField(max_length=45)
    unidad_medida = models.CharField(max_length=45)
    proveedor = models.ForeignKey('provedor.Proveedor', on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_sustancia