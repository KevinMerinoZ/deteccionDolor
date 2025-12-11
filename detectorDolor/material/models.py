from django.db import models

# Create your models here.
class Material(models.Model):
    idmateriales = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    material_fabricacion = models.CharField(max_length=45)
    piezas_disponibles = models.IntegerField()
    uso = models.CharField(max_length=45)
    proveedor = models.ForeignKey("provedor.Proveedor", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre