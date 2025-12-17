from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import SustanciaExperimental
from .forms import SustanciaExperimentalForm


# ------------------------------------------------------------
#  INDEX
# ------------------------------------------------------------
def pgSustanciaIndex(request):

    sustancias = SustanciaExperimental.objects.filter(
        is_active=True
    ).order_by('idsustanciaExperimental')

    paginator = Paginator(sustancias, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sustancias': page_obj.object_list,
    }
    return render(request, 'sustancia/index.html', context)


# ------------------------------------------------------------
#  CREAR
# ------------------------------------------------------------
def pgSustanciaCrear(request):

    if request.method == 'POST':
        form = SustanciaExperimentalForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sustanciaExperimental:indexSustancia')
    else:
        form = SustanciaExperimentalForm()

    return render(request, 'sustancia/crear.html', {'form': form})


# ------------------------------------------------------------
#  EDITAR
# ------------------------------------------------------------
def pgSustanciaEditar(request, idsustanciaExperimental):

    sustancia = get_object_or_404(
        SustanciaExperimental,
        idsustanciaExperimental=idsustanciaExperimental
    )

    if request.method == 'POST':
        form = SustanciaExperimentalForm(request.POST, instance=sustancia)

        if form.is_valid():
            form.save()
            return redirect('sustanciaExperimental:indexSustancia')
    else:
        form = SustanciaExperimentalForm(instance=sustancia)

    return render(request, 'sustancia/editar.html', {'form': form})


# ------------------------------------------------------------
#  ELIMINAR (LÓGICA)
# ------------------------------------------------------------
def pgSustanciaEliminar(request, idsustanciaExperimental):

    sustancia = get_object_or_404(
        SustanciaExperimental,
        idsustanciaExperimental=idsustanciaExperimental
    )

    sustancia.is_active = False
    sustancia.save()

    return redirect('sustanciaExperimental:indexSustancia')


# ------------------------------------------------------------
#  BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarSustancia(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    sustancias = SustanciaExperimental.objects.filter(is_active=True)

    if filtro == 'nombre':
        sustancias = sustancias.filter(
            nombre_sustancia__icontains=dato
        ).order_by('nombre_sustancia')

    elif filtro == 'proveedor':
        sustancias = sustancias.filter(
            proveedor__nombre_proveedor__icontains=dato
        ).order_by('proveedor__nombre_proveedor')

    else:
        sustancias = sustancias.order_by('idsustanciaExperimental')

    paginator = Paginator(sustancias, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string(
        'sustancia/tabla_resultados.html',
        {'sustancias': page_obj.object_list}
    )

    paginacion = render_to_string(
        'sustancia/paginacion.html',
        {'page_obj': page_obj}
    )

    return JsonResponse({
        'tabla': tabla,
        'paginacion': paginacion
    })
