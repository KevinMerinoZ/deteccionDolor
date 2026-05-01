from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import ActividadUsuario

@receiver(user_logged_out)
def cerrar_sesion_activa(sender, request, user, **kwargs):
    if user:
        sesionAct = ActividadUsuario.objects.filter(usuario__user__username=request.user.username, activo=True).last()
        print("La sesion activa es: ", sesionAct)

        if sesionAct:
            sesionAct.activo = 0
            sesionAct.save()