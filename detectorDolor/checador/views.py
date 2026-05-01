
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Checada
from zoneinfo import ZoneInfo
from collections import defaultdict
from django.utils.timezone import localtime
from django.utils import timezone
from django.utils.timezone import localtime

@login_required
def checador_panel(request):
    hoy = timezone.localdate()
    
    checada, creada = Checada.objects.get_or_create(
        usuario=request.user,
        fecha=hoy
    )

    if request.method == 'POST':
        if 'entrada' in request.POST and not checada.hora_entrada:            
            checada.hora_entrada = timezone.now()
            checada.save()

        elif 'salida' in request.POST and checada.hora_entrada and not checada.hora_salida:
            checada.hora_salida = timezone.now()
            checada.save()

        return redirect('checador:checador_panel')

    historial = Checada.objects.filter(
        usuario=request.user
    ).order_by('-fecha')

    return render(request, 'checador/panel.html', {
        'checada': checada,
        'historial': historial
    })

@login_required
def asistencia_admin(request):
    fecha_inicio = request.GET.get('inicio')
    fecha_fin = request.GET.get('fin')

    checadas = Checada.objects.select_related('usuario')

    if fecha_inicio and fecha_fin:
        checadas = checadas.filter(fecha__range=[fecha_inicio, fecha_fin])

    checadas = checadas.order_by('usuario', 'fecha')

    registros = []
    totales = defaultdict(float)  # ✅ SIEMPRE diccionario

    for c in checadas:
        if c.fecha.weekday() < 5:
            horas = c.horas_dia()

            if horas > 0:
                totales[c.usuario] += horas  # ✅ acumulación correcta

            registros.append({
                'usuario': c.usuario,
                'fecha': c.fecha,
                'entrada': c.hora_entrada,
                'salida': c.hora_salida,
                'asistencia': c.es_asistencia(),
                'horas': horas
            })
    totales = dict(totales)

    return render(request, 'checador/asistencia_admin.html', {
        'registros': registros,
        'totales': totales,  # ✅ se envía el diccionario
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })


