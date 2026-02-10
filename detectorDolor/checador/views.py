
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Checada
from zoneinfo import ZoneInfo

def checador_panel(request):
    hoy = timezone.now().date()

    checada, creada = Checada.objects.get_or_create(
        usuario=request.user,
        fecha=hoy
    )

    if request.method == 'POST':
        if 'entrada' in request.POST and not checada.hora_entrada:
            checada.hora_entrada = timezone.now().replace(tzinfo=ZoneInfo("America/Mexico_City"))
            checada.save()

        elif 'salida' in request.POST and checada.hora_entrada and not checada.hora_salida:
            checada.hora_salida = timezone.now().replace(tzinfo=ZoneInfo("America/Mexico_City"))
            checada.save()

        return redirect('checador:checador_panel')

    historial = Checada.objects.filter(
        usuario=request.user
    ).order_by('-fecha')

    return render(request, 'checador/panel.html', {
        'checada': checada,
        'historial': historial
    })

