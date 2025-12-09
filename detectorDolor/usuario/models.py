from django.db import models
from django.contrib.auth.models import User

# app_detectordolor/models.py
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')

    idUsuarios = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=55)
    apellido_paterno = models.CharField(max_length=45)
    apellido_materno = models.CharField(max_length=45, null=True, blank=True)
    correo = models.EmailField(max_length=55)
    fecha_registro = models.DateField()

    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"


class Proveedor(models.Model):
    idProveedor = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=45)
    contacto = models.CharField(max_length=45)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(max_length=25)
    direccion = models.CharField(max_length=45)
    tipo_insumo = models.CharField(max_length=15)
    observaciones = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_proveedor


class SustanciaExperimental(models.Model):
    idsustanciaExperimental = models.AutoField(primary_key=True)
    nombre_sustancia = models.CharField(max_length=45)
    tipo = models.CharField(max_length=25)
    consentracion = models.CharField(max_length=15)
    presentacion = models.CharField(max_length=45)
    unidad_medida = models.CharField(max_length=45)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_sustancia


class ProtocoloExperimental(models.Model):
    idprotocolosExperimentales = models.AutoField(primary_key=True)
    nombre_protocolo = models.CharField(max_length=45)
    objetivo_protocolo = models.CharField(max_length=45)
    sustancia_experimental = models.ForeignKey(SustanciaExperimental, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion_protocolo = models.CharField(max_length=100)
    consideraciones_eticas = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_protocolo


class Cita(models.Model):
    idcitas = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    protocolo_experimental = models.ForeignKey(ProtocoloExperimental, on_delete=models.CASCADE)
    estado = models.CharField(max_length=45)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cita {self.idcitas} - {self.usuario}"


class Farmaco(models.Model):
    idfarmacos = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    presentacion = models.CharField(max_length=15)
    tipo_farmaco = models.CharField(max_length=15)
    via_administracion = models.CharField(max_length=15)
    consentracion = models.CharField(max_length=15)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class SesionExperimental(models.Model):
    idsesionExperimental = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nombre_experimento = models.CharField(max_length=45)
    observaciones = models.CharField(max_length=45)
    numero_mediciones = models.IntegerField()
    farmaco = models.ForeignKey(Farmaco, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    protocolo_experimental = models.ForeignKey(ProtocoloExperimental, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_experimento


class ResultadoMedicion(models.Model):
    idresultadoMedicion = models.AutoField(primary_key=True)
    medicion_obtenida = models.CharField(max_length=20)
    numero_medicion = models.IntegerField()
    sesion_experimental = models.ForeignKey(SesionExperimental, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Medición {self.numero_medicion} ({self.sesion_experimental})"


class Material(models.Model):
    idmateriales = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    material_fabricacion = models.CharField(max_length=45)
    piezas_disponibles = models.IntegerField()
    uso = models.CharField(max_length=45)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
