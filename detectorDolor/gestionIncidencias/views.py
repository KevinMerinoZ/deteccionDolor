from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import IncidenciaExperimental
from .forms import IncidenciaExperimentalforms


# ------------------------------------------------------------
#  INDEX
# ------------------------------------------------------------
def IncidenciasIndex(request):

    incidencia = IncidenciaExperimental.objects.filter(is_active=True).order_by('idIncidencia')

    paginator = Paginator(incidencia, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'incidencias': page_obj.object_list,
    }
    return render(request, 'Incidencias/index.html', context)


# ------------------------------------------------------------
#  CREAR
# ------------------------------------------------------------
def IncidenciasCrear(request):

    if request.method == 'POST':
        form = IncidenciaExperimentalforms(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('gestionIncidencias:indexIncidencias')
    else:
        form = IncidenciaExperimentalforms(user=request.user)

    return render(request, 'Incidencias/crear.html', {'form': form})


# ------------------------------------------------------------
#  EDITAR
# ------------------------------------------------------------
def IncidenciasEditar(request, idIncidencia):

    incidencia = get_object_or_404(IncidenciaExperimental, idIncidencia=idIncidencia)

    if request.method == 'POST':
        form = IncidenciaExperimentalforms(request.POST, instance=incidencia, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('gestionIncidencias:indexIncidencias')
    else:
        form = IncidenciaExperimentalforms(instance=incidencia, user=request.user)

    return render(request, 'Incidencias/editar.html', {'form': form})

# ------------------------------------------------------------
#  ELIMINAR (LÓGICO)
# ------------------------------------------------------------
def IncidenciasEliminar(request, idIncidencia):

    incidencia = get_object_or_404(IncidenciaExperimental, idIncidencia=idIncidencia)
    incidencia.is_active = False
    incidencia.save()
    return redirect('gestionIncidencias:indexIncidencias')


# ------------------------------------------------------------
#  BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarIncidencia(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    incidencias = IncidenciaExperimental.objects.filter(is_active=True)

    if filtro == 'sesionExperimental':
        incidencias = incidencias.filter(idSesionExperimental__nombre_experimento__icontains=dato).order_by('idSesionExperimental__nombre_experimento')

    
    else:
        incidencias = incidencias.order_by('idIncidencia')

    paginator = Paginator(incidencias, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string('Incidencias/tabla_resultados.html', {
        'incidencias': page_obj.object_list
    })

    paginacion = render_to_string('Incidencias/paginacion.html', {
        'page_obj': page_obj
    })

    return JsonResponse({'tabla': tabla, 'paginacion': paginacion})