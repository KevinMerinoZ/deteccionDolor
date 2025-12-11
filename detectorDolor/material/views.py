from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Material
from .forms import MaterialForm
from provedor.models import Proveedor


# ------------------------------------------------------------
# INDEX
# ------------------------------------------------------------
def pgMaterialIndex(request):

    materiales = Material.objects.filter(is_active=True).order_by('idmateriales')

    paginator = Paginator(materiales, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'materiales': page_obj.object_list,
    }
    return render(request, 'material/index.html', context)


# ------------------------------------------------------------
# CREAR
# ------------------------------------------------------------
def pgMaterialCrear(request):

    if request.method == 'POST':
        form = MaterialForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('material:indexMaterial')

    else:
        form = MaterialForm()
        provedores = Proveedor.objects.filter(is_active=True)

    return render(request, 'material/crear.html', {'form': form, 'proveedores': provedores})


# ------------------------------------------------------------
# EDITAR
# ------------------------------------------------------------
def pgMaterialEditar(request, idmateriales):

    material = get_object_or_404(Material, idmateriales=idmateriales)

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)

        if form.is_valid():
            form.save()
            return redirect('material:indexMaterial')

    else:
        form = MaterialForm(instance=material)
        provedores = Proveedor.objects.filter(is_active=True)

    return render(request, 'material/editar.html', {'form': form, 'proveedores': provedores})


# ------------------------------------------------------------
# ELIMINAR (LÓGICA)
# ------------------------------------------------------------
def pgMaterialEliminar(request, idmateriales):

    material = get_object_or_404(Material, idmateriales=idmateriales)
    material.is_active = False
    material.save()

    return redirect('material:indexMaterial')


# ------------------------------------------------------------
# BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarMaterial(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    materiales = Material.objects.filter(is_active=True)

    # -----------------------------
    # Filtros dinámicos
    # -----------------------------
    if filtro == 'nombre':
        materiales = materiales.filter(nombre__icontains=dato).order_by('nombre')

    elif filtro == 'fabricacion':
        materiales = materiales.filter(material_fabricacion__icontains=dato).order_by('material_fabricacion')

    elif filtro == 'uso':
        materiales = materiales.filter(uso__icontains=dato).order_by('uso')

    elif filtro == 'proveedor':
        materiales = materiales.filter(proveedor__nombre_proveedor__icontains=dato).order_by('proveedor__nombre_proveedor')

    else:
        materiales = materiales.order_by('idmateriales')

    # -----------------------------
    # Paginación
    # -----------------------------
    paginator = Paginator(materiales, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string('material/tabla_resultados.html', {
        'materiales': page_obj.object_list
    })

    paginacion = render_to_string('material/paginacion.html', {
        'page_obj': page_obj
    })

    return JsonResponse({'tabla': tabla, 'paginacion': paginacion})
