from django.db import models

# Create your models here.
class LoteAnimales(models.Model):
    ESPECIE_RATA = 'rata'
    ESPECIE_RATON = 'raton'
    ESPECIES=[
        (ESPECIE_RATA, 'Rata'),
        (ESPECIE_RATON, 'Ratón'),
    ]

    GENERO_M = 'macho'
    GENERO_H = 'hembra'
    GENEROS=[
        (GENERO_M, 'Macho'),
        (GENERO_H, 'Hembra'),
    ]

    ESTADO_SANO = 'sano'
    ESTADO_EXPERIMENTACION = 'experimentacion'
    ESTADO_BAJA = 'baja'
    ESTADOS = [
        (ESTADO_SANO, 'Sano'),
        (ESTADO_EXPERIMENTACION, 'En experimentación'),
        (ESTADO_BAJA, 'Baja'),
    ]

    idlotesAnimales = models.AutoField(primary_key=True)
    especie = models.CharField(max_length=10, choices=ESPECIES)
    cantidad_animales = models.IntegerField()
    genero = models.CharField(max_length=10, choices=GENEROS)
    peso_ingreso = models.FloatField()
    condicion_experimental = models.CharField(max_length=45, null=True, blank=True)
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=50, choices=ESTADOS)
    cepa = models.CharField(max_length=15)
    fecha_baja = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey("usuario.Usuario", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f"Lote {self.idlotesAnimales} - {self.especie}"
