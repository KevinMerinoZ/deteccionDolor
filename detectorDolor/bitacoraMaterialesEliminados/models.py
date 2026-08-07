from django.db import models

# Create your models here.
class BitacoraMaterialesEliminados(models.Model):
    idBitacora = models.AutoField(primary_key=True)
    material = models.ForeignKey("material.Material", on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    fecha_eliminacion = models.DateTimeField()
    motivo = models.TextField()
    usuario_responsable = models.ForeignKey("usuario.Usuario", on_delete=models.PROTECT, related_name="eliminaciones_realizadas")
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)