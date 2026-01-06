from django.db import models

# Create your models here.
class SesionExperimental(models.Model):
    idsesionExperimental = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nombre_experimento = models.CharField(max_length=45)
    observaciones = models.CharField(max_length=45)
    numero_mediciones = models.IntegerField()
    farmaco = models.ForeignKey("farmaco.Farmaco", on_delete=models.CASCADE)
    usuario = models.ForeignKey("usuario.Usuario", on_delete=models.CASCADE)
    protocolo_experimental = models.ForeignKey('protocoloExperimental.ProtocoloExperimental', on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_experimento
    
class ResultadoMedicion(models.Model):
    idresultadoMedicion = models.AutoField(primary_key=True)
    medicion_obtenida = models.CharField(max_length=20)
    numero_medicion = models.IntegerField()
    sesion_experimental = models.ForeignKey('sesionExperimental.SesionExperimental', on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Medición {self.numero_medicion} ({self.sesion_experimental})"