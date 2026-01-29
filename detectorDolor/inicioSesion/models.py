from django.db import models
from django.utils import timezone

# Create your models here.
class PassVerificacion(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaExpiro = models.DateTimeField()
    usado = models.BooleanField(default=False)

    def is_valid(self):
        return (
            not self.usado and
            timezone.now() <= self.fechaExpiro
        )