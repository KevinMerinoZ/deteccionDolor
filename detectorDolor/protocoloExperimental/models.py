from django.db import models

# Create your models here.
class ProtocoloExperimental(models.Model):
    idprotocolosExperimentales = models.AutoField(primary_key=True)
    nombre_protocolo = models.CharField(max_length=45)
    objetivo_protocolo = models.CharField(max_length=45)
    sustancia_experimental = models.ForeignKey('sustanciaExperimental.SustanciaExperimental', on_delete=models.SET_NULL, null=True, blank=True)
    descripcion_protocolo = models.CharField(max_length=100)
    consideraciones_eticas = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_protocolo
    
    class Meta:
        db_table = 'ProtocoloExperimental'
