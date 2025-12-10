from django.db import models

# Create your models here.
class Proveedor(models.Model):
    idProveedor = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=45)
    contacto = models.CharField(max_length=45)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(max_length=55)
    direccion = models.CharField(max_length=45)
    tipo_insumo = models.CharField(max_length=15) # fármaco, sustancia experimental o material
    observaciones = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_proveedor