from django.db import models
from django.utils import timezone

# Create your models here.
class Farmaco(models.Model):
    TIPOS_FARMACOS = [
        ('ANESTESICO_GENERAL', 'Anestésico general'),
        ('ANESTESICO_LOCAL', 'Anestésico local'),
        ('SEDANTE', 'Sedante / Tranquilizante'),
        ('ANALGESICO_OPIOIDE', 'Analgésico opioide'),
        ('ANALGESICO_AINE', 'Analgésico AINE'),
        ('ANALGESICO_NEUROMODULADOR', 'Analgésico adyuvante / Neuromodulador'),
        ('INHIBIDOR_ENZIMATICO', 'Inhibidor enzimático experimental'),
        ('MODULADOR_CANALES', 'Modulador de canales iónicos'),
        ('ANTAGONISTA_TRP', 'Antagonista de receptores TRP'),
        ('AGENTE_ALGESIOGENICO', 'Agente algesiogénico / Inductor de dolor'),
    ]

    PRESENTACIONES = [
        ('TABLETA', 'Tableta'),
        ('AMPOLLA', 'Ampolla'),
        ('GRANULADO', 'Granulado'),
        ('CAPSULA', 'Cápsula'),
        ('CREMA', 'Crema'),
        ('POMADA', 'Pomada'),
        ('PASTA', 'Pasta'),
        ('GEL', 'Gel'),
        ('SOLUCION_ORAL', 'Solución oral'),
        ('SUSPENSION_ORAL', 'Suspensión oral'),
        ('EMULSION_ORAL', 'Emulsión oral'),
        ('JARABE', 'Jarabe'),
        ('VIAL', 'Vial'),
        ('INFUSION', 'Infusión'),
    ]


    TIPOS_FARMACO = []
    idfarmacos = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    presentacion = models.CharField(max_length=30, choices=PRESENTACIONES)
    tipo_farmaco = models.CharField(max_length=25, choices=TIPOS_FARMACOS)
    fecha_llegada = models.DateField()
    fecha_abierto = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre