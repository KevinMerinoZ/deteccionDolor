from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import SesionExperimental
from usuario.models import Usuario
from .forms import SesionExperimentalForm

from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime
import io
import xlsxwriter

# ------------------------------------------------------------
#  INDEX
# ------------------------------------------------------------
def pgSesionIndex(request):

    sesiones = SesionExperimental.objects.filter(
        is_active=True
    ).order_by('-fecha')

    paginator = Paginator(sesiones, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sesiones': page_obj.object_list,
    }
    return render(request, 'sesion/index.html', context)


# ------------------------------------------------------------
#  CREAR
# ------------------------------------------------------------
def pgSesionCrear(request):

    if request.method == 'POST':
        form = SesionExperimentalForm(request.POST, user = request.user)

        if form.is_valid():
            sesion = form.save(commit=False)

            if not request.user.groups.filter(name='administrador').exists():
                sesion.usuario = request.user.usuario  

            sesion.save()
            return redirect('sesionExperimental:indexSesion')

    else:
        form = SesionExperimentalForm(user = request.user)

    return render(request, 'sesion/crear.html', {'form': form})


# ------------------------------------------------------------
#  EDITAR
# ------------------------------------------------------------
def pgSesionEditar(request, idSesion):

    sesion = get_object_or_404(
        SesionExperimental,
        idsesionExperimental=idSesion
    )

    if request.method == 'POST':
        form = SesionExperimentalForm(request.POST, instance=sesion, user = request.user)

        if form.is_valid():
            form.save()
            return redirect('sesionExperimental:indexSesion')

    else:
        form = SesionExperimentalForm(instance=sesion, user = request.user)

    return render(request, 'sesion/editar.html', {'form': form})


# ------------------------------------------------------------
#  ELIMINAR (LÓGICA)
# ------------------------------------------------------------
def pgSesionEliminar(request, idSesion):

    sesion = get_object_or_404(
        SesionExperimental,
        idsesionExperimental=idSesion
    )
    sesion.is_active = False
    sesion.save()

    return redirect('sesionExperimental:indexSesion')

# ------------------------------------------------------------
#  REPORTE DE CANTIDAD DE SESIONES POR FECHA
# ------------------------------------------------------------

def pgReporteCantFecha(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fechaInicio')
        fecha_fin = request.POST.get('fechaFin')

        if not fecha_inicio or not fecha_fin:
            return HttpResponse("Debe proporcionar fecha_inicio y fecha_fin")

        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        sesiones = SesionExperimental.objects.filter(
            fecha__range=(fecha_inicio, fecha_fin)
        )

        conteo = sesiones.values('estado').annotate(total=Count('estado'))

        finalizadas = 0
        pendientes = 0

        for item in conteo:
            if item['estado']:
                finalizadas = item['total']
            else:
                pendientes = item['total']

        # Crear archivo en memoria
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Reporte")

        # Formatos
        bold = workbook.add_format({'bold': True})
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14
        })

        # Título
        worksheet.merge_range('A1:D1', 'Reporte de Estado de Sesiones Experimentales', title_format)

        worksheet.write('A3', 'Intervalo:', bold)
        worksheet.write('B3', f'{fecha_inicio} a {fecha_fin}')

        # Encabezados
        worksheet.write('A5', 'Estado', bold)
        worksheet.write('B5', 'Cantidad', bold)

        # Datos
        worksheet.write('A6', 'Finalizadas')
        worksheet.write('B6', finalizadas)

        worksheet.write('A7', 'Pendientes')
        worksheet.write('B7', pendientes)

        # Crear gráfica
        chart = workbook.add_chart({'type': 'column'})

        chart.add_series({
            'name': 'Sesiones',
            'categories': '=Reporte!$A$6:$A$7',
            'values': '=Reporte!$B$6:$B$7',
            'data_labels': {'value': True},
        })

        chart.set_title({'name': 'Sesiones por Estado'})
        chart.set_x_axis({'name': 'Estado'})
        chart.set_y_axis({'name': 'Cantidad'})

        worksheet.insert_chart('D5', chart)

        workbook.close()
        output.seek(0)

        # Respuesta HTTP para descarga automática
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        nombreArchivo = "reporte_sesiones_experimentales"+ str(datetime.now()) +".xlsx"

        response['Content-Disposition'] = f'attachment; filename={nombreArchivo}'

        return response
    
    return render(request, 'sesion/reporteCantFecha.html')


# ------------------------------------------------------------
#  BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarSesion(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    es_admin = request.user.groups.filter(name='administrador').exists()

    if request.user.groups.first().name == 'administrador':
        sesiones = SesionExperimental.objects.filter(is_active=True)
    else:
        usuarioAct = request.user
        sesiones = SesionExperimental.objects.filter(is_active=True, usuario_id__user__username=usuarioAct)

    if filtro == 'experimento':
        sesiones = sesiones.filter(
            nombre_experimento__icontains=dato
        ).order_by('nombre_experimento')

    elif filtro == 'farmaco':
        sesiones = sesiones.filter(
            farmaco_id__nombre__icontains=dato
        ).order_by('farmaco_id__nombre')

    elif filtro == 'usuario':
        sesiones = sesiones.filter(
            usuario_id__nombre__icontains=dato
        ).order_by('usuario_id__nombre')

    elif filtro == 'protocolo':
        sesiones = sesiones.filter(
            protocolo_experimental_id__nombre_protocolo__icontains=dato
        ).order_by('protocolo_experimental_id__nombre_protocolo')
    else:
        sesiones = sesiones.order_by('idsesionExperimental')

    paginator = Paginator(sesiones, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string(
        'sesion/tabla_resultados.html',
        {'sesiones': page_obj.object_list, 'es_administrador': es_admin}
    )

    paginacion = render_to_string(
        'sesion/paginacion.html',
        {'page_obj': page_obj}
    )

    return JsonResponse({
        'tabla': tabla,
        'paginacion': paginacion
    })
