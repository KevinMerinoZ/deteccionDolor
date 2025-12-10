from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Farmaco
from .forms import FarmacoForm


# ------------------------------------------------------------
#  INDEX
# ------------------------------------------------------------
def pgFarmacoIndex(request):

    farmacos = Farmaco.objects.filter(is_active=True).order_by('idfarmacos')

    paginator = Paginator(farmacos, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'farmacos': page_obj.object_list,
    }
    return render(request, 'farmaco/index.html', context)


# ------------------------------------------------------------
#  CREAR
# ------------------------------------------------------------
def pgFarmacoCrear(request):

    if request.method == 'POST':
        form = FarmacoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('farmaco:indexFarmaco')

    else:
        form = FarmacoForm()

    return render(request, 'farmaco/crear.html', {'form': form})


# ------------------------------------------------------------
#  EDITAR
# ------------------------------------------------------------
def pgFarmacoEditar(request, idfarmacos):

    farmaco = get_object_or_404(Farmaco, idfarmacos=idfarmacos)

    if request.method == 'POST':
        form = FarmacoForm(request.POST, instance=farmaco)

        if form.is_valid():
            form.save()
            return redirect('farmaco:indexFarmaco')

    else:
        form = FarmacoForm(instance=farmaco)

    return render(request, 'farmaco/editar.html', {'form': form})


# ------------------------------------------------------------
#  ELIMINAR (LÓGICO)
# ------------------------------------------------------------
def pgFarmacoEliminar(request, idfarmacos):

    farmaco = get_object_or_404(Farmaco, idfarmacos=idfarmacos)
    farmaco.is_active = False
    farmaco.save()

    return redirect('farmaco:indexFarmaco')


# ------------------------------------------------------------
#  BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarFarmaco(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    farmacos = Farmaco.objects.filter(is_active=True)

    if filtro == 'nombre':
        farmacos = farmacos.filter(nombre__icontains=dato).order_by('nombre')

    elif filtro == 'presentacion':
        farmacos = farmacos.filter(presentacion__icontains=dato).order_by('presentacion')

    else:
        farmacos = farmacos.order_by('idfarmacos')

    paginator = Paginator(farmacos, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string('farmaco/tabla_resultados.html', {
        'farmacos': page_obj.object_list
    })

    paginacion = render_to_string('farmaco/paginacion.html', {
        'page_obj': page_obj
    })

    return JsonResponse({'tabla': tabla, 'paginacion': paginacion})
