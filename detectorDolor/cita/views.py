from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from django.utils import timezone

from .models import Cita
from usuario.models import Usuario, Notificacion
from .forms import CitaForm

import io
import xlsxwriter
from datetime import datetime, timedelta

# ------------------------------------------------------------
#  INDEX
# ------------------------------------------------------------
def pgCitaIndex(request):

    citas = Cita.objects.filter(is_active=True).order_by('idcitas')

    paginator = Paginator(citas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'citas': page_obj.object_list,
    }

    return render(request, 'cita/index.html', context)


# ------------------------------------------------------------
#  CREAR
# ------------------------------------------------------------
def pgCitaCrear(request):
    if request.method == 'POST':
        form = CitaForm(request.POST, user = request.user)

        if form.is_valid():
            cita = form.save(commit=False)

            # Usuario normal
            if not request.user.groups.filter(name='administrador').exists():
                cita.usuario = request.user.usuario  # o request.user si es FK directo

            usuario_cita = cita.usuario

            cita.save()
            registrarNotificacion(usuario_cita, 'Nueva Cita Registrada', f'El usuario {usuario_cita} registró una nueva cita para la fecha {cita.fechaInicio}.')
            return redirect('cita:indexCita')
    else:
        form = CitaForm(user = request.user)

    return render(request, 'cita/crear.html', {'form': form})

# ----------------------------------------------------------------------
# Registrar una notificación
# ----------------------------------------------------------------------
def buscarCitaPendiente(request):
    citas = Cita.objects.filter(is_active=True, estado='Asignada')

    flagCitasPendientes = citas.exists()
    flagCitasSigDia = False
    ahora = timezone.now()

    if(flagCitasPendientes):
        for cita in citas:
            diferencia = cita.fechaInicio - ahora

            # Si la cita es mañana (entre 0 y 1 día)
            if timedelta(0) < diferencia <= timedelta(days=1):
                flagCitasSigDia = True

                registrarNotificacion(
                    cita.usuario,
                    'Cita Pendiente',
                    f'La cita programada para el día {cita.fechaInicio} empezará mañana.'
                )

    return JsonResponse({
        'existenCitasPendientes': flagCitasPendientes,
        'existenCitasSigDia': flagCitasSigDia

    })

# ----------------------------------------------------------------------
# Registrar una notificación
# ----------------------------------------------------------------------

def registrarNotificacion(usuario_cita, titulo, mensaje):
    usuario = Usuario.objects.filter(is_active=True, user__groups__name='administrador')
    objeto = Cita.objects.filter(is_active=True, usuario=usuario_cita).last() 
    for admin in usuario:
        notificacion = Notificacion(
            tipo=Notificacion.TIPO_CITA,
            id_objeto=objeto.idcitas,  # ID de la cita o sesión activa relacionada
            usuario=admin,
            titulo=titulo,
            mensaje=mensaje,
            fecha_creacion=timezone.now()
        )
        notificacion.save()


# ------------------------------------------------------------
#  EDITAR
# ------------------------------------------------------------
def pgCitaEditar(request, idcitas):

    cita = get_object_or_404(Cita, idcitas=idcitas, is_active=True)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita, user = request.user)

        if form.is_valid():
            form.save()
            return redirect('cita:indexCita')
    else:
        form = CitaForm(instance=cita, user = request.user)

    return render(request, 'cita/editar.html', {'form': form})


# ------------------------------------------------------------
#  ELIMINAR (LÓGICA)
# ------------------------------------------------------------
def pgCitaEliminar(request, idcitas):

    cita = get_object_or_404(Cita, idcitas=idcitas)
    cita.is_active = False
    cita.save()

    return redirect('cita:indexCita')

def cambiarEstadoCita(request, idcitas, nuevo_estado):
    cita = get_object_or_404(Cita, idcitas=idcitas)

    if nuevo_estado in dict(Cita.ESTADOS).keys():
        cita.estado = nuevo_estado
        cita.save()

    return redirect('cita:indexCita')

# ------------------------------------------------------------
#  REPORTE GENERAL DE CITAS
# ------------------------------------------------------------
def reporteGeneralCitas(request):
    usuarios = Usuario.objects.filter(is_active=True)

    if request.method == 'GET':
        return render(request, 'cita/reporteGneralC.html', {'usuarios': usuarios})

    fecha_inicio = request.POST.get('fechaInicio')
    fecha_fin = request.POST.get('fechaFin')
    usuario = request.POST.get('usuario')

    if not fecha_inicio or not fecha_fin:
        return HttpResponse("Debe proporcionar un rango de fechas")

    # Convertir a datetime
    fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio, "%Y-%m-%d"))
    fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin, "%Y-%m-%d"))
    # fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    # fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

    citas = Cita.objects.filter(
        fechaInicio__range=(fecha_inicio, fecha_fin),
        # fechaInicio__date__gte=fecha_inicio,
        # fechaInicio__date__lte=fecha_fin
    )

    # Filtro opcional por usuario
    if usuario:
        citas = citas.filter(usuario__user__username=usuario, is_active=True)

    # Contadores para gráfica
    realizadas = 0
    canceladas = 0
    pendientes = 0

    # Crear Excel
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Citas")

    # FORMATOS
    titulo = workbook.add_format({
        'bold': True,
        'align': 'center',
        'font_size': 16
    })

    encabezado = workbook.add_format({
        'bold': True,
        'border': 1,
        'align': 'center'
    })

    celda = workbook.add_format({
        'border': 1,
        'align': 'center'
    })

    fecha_format = workbook.add_format({
        'num_format': 'yyyy-mm-dd hh:mm',
        'border': 1
    })

    # Columnas
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 15)

    # Título
    worksheet.merge_range('A1:E1', 'Reporte de Citas de Laboratorio', titulo)

    # Encabezados
    headers = ['Fecha y Hora', 'Protocolo', 'Duración (min)', 'Sala', 'Estado']

    for col, header in enumerate(headers):
        worksheet.write(2, col, header, encabezado)

    # Llenar datos
    row = 3

    for cita in citas:

        duracion = int((cita.fechaFin - cita.fechaInicio).total_seconds() / 60)

        # Mapear estado
        if cita.estado == Cita.ESTADO_FINALIZADA:
            estado = 'Realizada'
            realizadas += 1
        elif cita.estado == Cita.ESTADO_CANCELADA:
            estado = 'Cancelada'
            canceladas += 1
        else:
            estado = 'Pendiente'
            pendientes += 1

        fechaInicio_naive = cita.fechaInicio.replace(tzinfo=None)
        worksheet.write_datetime(row, 0, fechaInicio_naive, fecha_format)
        worksheet.write(row, 1, str(cita.protocolo_experimental), celda)
        worksheet.write(row, 2, duracion, celda)
        worksheet.write(row, 3, str(cita.sala_laboratorio), celda)
        worksheet.write(row, 4, estado, celda)

        row += 1

    # Datos para gráfica
    worksheet.write('G3', 'Estado')
    worksheet.write('H3', 'Cantidad')

    worksheet.write('G4', 'Realizadas')
    worksheet.write('H4', realizadas)

    worksheet.write('G5', 'Canceladas')
    worksheet.write('H5', canceladas)

    worksheet.write('G6', 'Pendientes')
    worksheet.write('H6', pendientes)

    # Crear gráfica de pastel
    chart = workbook.add_chart({'type': 'pie'})

    chart.add_series({
        'name': 'Estado de Citas',
        'categories': '=Citas!$G$4:$G$6',
        'values': '=Citas!$H$4:$H$6',
        'data_labels': {'percentage': True},
    })

    chart.set_title({'name': 'Distribución de Citas'})

    worksheet.insert_chart('G8', chart)

    workbook.close()
    output.seek(0)

    # Descargar archivo
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    nombre_archivo = f"reporte_citas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'

    return response

# ------------------------------------------------------------
#  BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarCita(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    es_admin = request.user.groups.filter(name='administrador').exists()

    if request.user.groups.first().name == 'administrador':
        citas = Cita.objects.filter(is_active=True)
    else:
        usuarioAct = request.user
        citas = Cita.objects.filter(is_active=True, usuario_id__user__username=usuarioAct)

    if filtro == 'usuario':
        citas = citas.filter(
            usuario__nombre__icontains=dato
        ).order_by('usuario__nombre')

    elif filtro == 'protocolo':
        citas = citas.filter(
            protocolo_experimental__nombre_protocolo__icontains=dato
        ).order_by('protocolo_experimental__nombre_protocolo')

    elif filtro == 'fecha':
        citas = citas.filter(fechaInicio__icontains=dato).order_by('fechaInicio')

    else:
        citas = citas.order_by('idcitas')

    paginator = Paginator(citas, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string('cita/tabla_resultados.html', {
        'citas': page_obj.object_list,
        'es_administrador': es_admin
    })

    paginacion = render_to_string('cita/paginacion.html', {
        'page_obj': page_obj
    })

    return JsonResponse({
        'tabla': tabla,
        'paginacion': paginacion
    })
