from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import SesionExperimental
from .forms import SesionExperimentalForm


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
        form = SesionExperimentalForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sesionExperimental:indexSesion')

    else:
        form = SesionExperimentalForm()

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
        form = SesionExperimentalForm(request.POST, instance=sesion)

        if form.is_valid():
            form.save()
            return redirect('sesionExperimental:indexSesion')

    else:
        form = SesionExperimentalForm(instance=sesion)

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
#  BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarSesion(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    sesiones = SesionExperimental.objects.filter(is_active=True)

    if filtro == 'fecha':
        sesiones = sesiones.filter(fecha__icontains=dato).order_by('-fecha')

    elif filtro == 'experimento':
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
        {'sesiones': page_obj.object_list}
    )

    paginacion = render_to_string(
        'sesion/paginacion.html',
        {'page_obj': page_obj}
    )

    return JsonResponse({
        'tabla': tabla,
        'paginacion': paginacion
    })
