from django.db import models


class SustanciaExperimental(models.Model):
    PRESENTACION_SOLIDA = 'solida'
    PRESENTACION_SEMISOLIDA = 'semisolida'
    PRESENTACION_LIQUIDA = 'liquida'
    PRESENTACIONES = [
        (PRESENTACION_SOLIDA, 'Sólida'),
        (PRESENTACION_SEMISOLIDA, 'Semisólida'),
        (PRESENTACION_LIQUIDA, 'Líquida'),
    ]

    UNIDAD_MEDIDA_G = 'g'
    UNIDAD_MEDIDA_MG = 'mg'
    UNIDAD_MEDIDA_L = 'L'
    UNIDAD_MEDIDA_ML = 'ml'
    UNIDADES_MEDIDA = [
        (UNIDAD_MEDIDA_G, 'gramos (g)'),
        (UNIDAD_MEDIDA_MG, 'miligramos (mg)'),
        (UNIDAD_MEDIDA_L, 'litros (L)'),
        (UNIDAD_MEDIDA_ML, 'mililitros (ml)'),
    ]

    idsustanciaExperimental = models.AutoField(primary_key=True)
    nombre_sustancia = models.CharField(max_length=45)
    tipo = models.CharField(max_length=25)
    consentracion = models.CharField(max_length=15, default='')
    presentacion = models.CharField(max_length=15, choices=PRESENTACIONES)
    unidad_medida = models.CharField(max_length=5, choices=UNIDADES_MEDIDA)
    proveedor = models.ForeignKey('provedor.Proveedor', on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_sustancia