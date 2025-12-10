from django.db import models

# Create your models here.
class LoteAnimales(models.Model):
    idlotesAnimales = models.AutoField(primary_key=True)
    especie = models.CharField(max_length=15)
    cantidad_animales = models.IntegerField()
    genero = models.CharField(max_length=10)
    peso_ingreso = models.FloatField()
    condicion_experimental = models.CharField(max_length=45, null=True, blank=True)
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=50)
    cepa = models.CharField(max_length=15)
    fecha_baja = models.DateField(null=True, blank=True)
    observaciones = models.CharField(max_length=45, null=True, blank=True)
    usuario = models.ForeignKey("usuario.Usuario", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f"Lote {self.idlotesAnimales} - {self.especie}"
