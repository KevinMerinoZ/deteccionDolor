from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import ActividadUsuario

class CerrarSesionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                actividadU = ActividadUsuario.objects.filter(usuario__user__username=request.user.username).last()
                if not actividadU.activo:
                    logout(request)
                    return redirect('inicioSesion:login')
            except ActividadUsuario.DoesNotExist:
                logout(request)
                return redirect('inicioSesion:login')

        response = self.get_response(request)
        return response