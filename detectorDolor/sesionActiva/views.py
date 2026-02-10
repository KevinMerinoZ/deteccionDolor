from django.shortcuts import render
from .models import ActividadUsuario
from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.http import JsonResponse

# Create your views here.
def indexSesion(request):

    return render(request, 'sesion/index.html')

def tiempoSesion(request):
    actividad = ActividadUsuario.objects.filter(usuario__user__username=request.user).last()

    if actividad:
        if not actividad.fechaFin:
            actividad.fechaFin = actividad.fechaInicio + timedelta(seconds=15)
        else:
            actividad.fechaFin = actividad.fechaFin + timedelta(seconds=15)

        actividad.save()
    
        return JsonResponse({"status":"ok"})

    return JsonResponse({"status": "algo andaba mal"})

