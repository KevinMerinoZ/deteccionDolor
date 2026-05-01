from django.shortcuts import render
from .models import ActividadUsuario
import datetime
from django.utils import timezone
from django.contrib.auth import logout
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import HttpResponse
import io
import calendar
import xlsxwriter

from usuario.models import Usuario

# Create your views here.
def indexSesion(request):
    actividadUsuarios = ActividadUsuario.objects.filter(activo=True).order_by('idActividad')
    paginator = Paginator(actividadUsuarios, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    print(timezone.now())

    context = {
        'actividadUsuarios': page_obj.object_list,
        'page_obj': page_obj,
    }

    return render(request, 'sesionAct/index.html', context)

def tiempoSesion(request):
    actividad = ActividadUsuario.objects.filter(usuario__user__username=request.user, activo=True).last()

    if actividad:
        if not actividad.ultimaActividad:
            actividad.ultimaActividad = actividad.fechaInicio + datetime.timedelta(seconds=15)
        else:
            actividad.ultimaActividad = timezone.now()

        actividad.save()
    
        return JsonResponse({"status":"ok"})

    return JsonResponse({"status": "cerrado"})


def cerrarSesion(request, idUsuario):
    actividadUsuario = ActividadUsuario.objects.filter(usuario__idUsuarios=idUsuario, activo=True).last()

    if actividadUsuario:
        actividadUsuario.activo = False
        actividadUsuario.ultimaActividad = timezone.now()
        actividadUsuario.save()

    return render(request, 'sesionAct/index.html')

def reporte_actividad_usuario(request):
    usuarios = Usuario.objects.filter(is_active=True).order_by('user__username')

    if request.method == "POST":
        usuario_matricula = request.POST.get("usuario")
        fecha_inicio = request.POST.get("mesInicio")
        fecha_fin = request.POST.get("mesFin")

        usuario = usuarios.filter(user__username=usuario_matricula).first()

        anioInicio, mesInicio = map(int, fecha_inicio.split("-"))
        fecha_inicio = timezone.make_aware(
            datetime.datetime(anioInicio, mesInicio, 1)
        )

        anioFin, mesFin = map(int, fecha_fin.split("-"))
        ultimo_dia_mes = calendar.monthrange(anioFin, mesFin)[1]
        fecha_fin = timezone.make_aware(
            datetime.datetime(anioFin, mesFin, ultimo_dia_mes, 23, 59, 59)
        )

        actividades = ActividadUsuario.objects.filter(
            usuario=usuario,
            fechaInicio__range=(fecha_inicio, fecha_fin)
        ).order_by("fechaInicio")

        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Actividad Usuario")

        worksheet.set_column('A:A', 11)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 30)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('G:G', 35)
        worksheet.set_column('H:H', 35)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:J', 40)
        worksheet.set_column('K:K', 35)

        encabezados = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
        })

        celda_normal = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
        })

        headers = [
            "Username",
            "Nombre",
            "Apellido paterno",
            "Apellido materno",
            "Correo Electrónico",
            "Dirección IP",
            "Fecha de inicio de sesión y hora",
            "Fecha y hora de última actividad",
            "Horas de actividad",
            "Tiempo de actividad en el mes en horas",
            "Tiempo de actividad Total en horas"
        ]

        for col, h in enumerate(headers):
            worksheet.write(0, col, h, encabezados)

        row = 1
        horas_mes = 0
        total_horas = 0

        meses = {}

        for actividad in actividades:

            mes = actividad.fechaInicio.month
            anio = actividad.fechaInicio.year

            clave = (mes, anio)

            if clave not in meses:
                meses[clave] = []

            meses[clave].append(actividad)

        for (mes, anio), acts in meses.items():
            
            horas_mes = 0
            rows_mes = 0

            nombre_mes = f"{calendar.month_name[mes]} - {anio}"
            row += 1
            worksheet.merge_range(f'A{row}:J{row}', nombre_mes, encabezados)

            for act in acts:

                tiempo = act.ultimaActividad - act.fechaInicio
                horas = tiempo.total_seconds() / 3600

                horas_mes += horas

                worksheet.write(row, 0, usuario.user.username, celda_normal)
                worksheet.write(row, 1, usuario.nombre, celda_normal)
                worksheet.write(row, 2, usuario.apellido_paterno, celda_normal)
                worksheet.write(row, 3, usuario.apellido_materno, celda_normal)
                worksheet.write(row, 4, usuario.correo, celda_normal)
                worksheet.write(row, 5, act.direccionIP, celda_normal)
                worksheet.write(row, 6, str(act.fechaInicio), celda_normal)
                worksheet.write(row, 7, str(act.ultimaActividad), celda_normal)
                worksheet.write(row, 8, round(horas, 2), celda_normal)

                rows_mes += 1
                row += 1

            worksheet.merge_range(f'J{row-rows_mes+1}:J{row}', round(horas_mes, 2), celda_normal)

            total_horas += horas_mes
            row += 1

        worksheet.write(2, 10, round(total_horas, 2), celda_normal)

        workbook.close()

        output.seek(0)

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        nombreArchivo = f"reporte_actividad_usuario_{usuario.user.username}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        response['Content-Disposition'] = f'attachment; filename="{nombreArchivo}"'

        return response
    
    return render(request, 'sesionAct/reporteActUsuario.html', {'usuarios': usuarios})


def buscarActividadUsuario(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    if filtro == 'nombre':
        actividadUsuarios = ActividadUsuario.objects.filter(usuario__nombre__icontains=dato, activo=True).order_by('usuario__nombre')
    elif filtro == 'apellidoP':
        actividadUsuarios = ActividadUsuario.objects.filter(usuario__apellido_paterno__icontains=dato, activo=True).order_by('usuario__apellido_paterno')
    elif filtro == 'matricula':
        actividadUsuarios = ActividadUsuario.objects.filter(usuario__matricula__icontains=dato, activo=True).order_by('usuario__matricula')
    elif filtro == 'correo':
        actividadUsuarios = ActividadUsuario.objects.filter(usuario__correo__icontains=dato, activo=True).order_by('usuario__correo')
    else:
        actividadUsuarios = ActividadUsuario.objects.filter(activo=True).order_by('idActividad')

    paginator = Paginator(actividadUsuarios, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string('sesionAct/tabla_resultados.html', {
        'actividadUsuarios': page_obj.object_list,
    })

    paginacion = render_to_string('sesionAct/paginacion.html', {
        'page_obj': page_obj
    })

    return JsonResponse({
        'tabla': tabla,
        'paginacion': paginacion
    })