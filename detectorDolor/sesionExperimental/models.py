from django.db import models

# Create your models here.
class SesionExperimental(models.Model):
    idsesionExperimental = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nombre_experimento = models.CharField(max_length=45)
    observaciones = models.CharField(max_length=45)
    farmaco = models.ForeignKey("farmaco.Farmaco", on_delete=models.CASCADE)
    usuario = models.ForeignKey("usuario.Usuario", on_delete=models.CASCADE)
    protocolo_experimental = models.ForeignKey('protocoloExperimental.ProtocoloExperimental', on_delete=models.CASCADE)
    noMediciones1 = models.IntegerField(default=0)
    intervaloTemp1 = models.IntegerField(default=0)
    noMediciones2 = models.IntegerField(null =True, blank=True)
    intervaloTemp2 = models.IntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_experimento
    
class ResultadoMedicion(models.Model):
    NIVEL_DOLOR_1 = 1
    NIVEL_DOLOR_2 = 2
    NIVEL_DOLOR_3 = 3

    NIVELES_DOLOR = [
        (NIVEL_DOLOR_1, 'Sin dolor'),
        (NIVEL_DOLOR_2, 'Dolor leve'),
        (NIVEL_DOLOR_3, 'Dolor intenso'),
    ]

    idresultadoMedicion = models.AutoField(primary_key=True)
    noRaton = models.IntegerField()
    nivelDolor = models.IntegerField(choices=NIVELES_DOLOR)
    confianza = models.DecimalField(max_digits=6, decimal_places=3) 
    numero_medicion = models.IntegerField()
    sesion_experimental = models.ForeignKey('sesionExperimental.SesionExperimental', on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Medición {self.numero_medicion} ({self.sesion_experimental})"