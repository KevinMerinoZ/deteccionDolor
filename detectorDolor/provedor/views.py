from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Proveedor
from .forms import ProveedorForm


# ------------------------------------------------------------
#  INDEX
# ------------------------------------------------------------
def pgProveedorIndex(request):

    proveedores = Proveedor.objects.filter(is_active=True).order_by('idProveedor')

    paginator = Paginator(proveedores, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'proveedores': page_obj.object_list,
    }
    return render(request, 'provedor/index.html', context)


# ------------------------------------------------------------
#  CREAR
# ------------------------------------------------------------
def pgProveedorCrear(request):

    if request.method == 'POST':
        form = ProveedorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('provedor:indexProveedor')

    else:
        form = ProveedorForm()

    return render(request, 'provedor/crear.html', {'form': form})


# ------------------------------------------------------------
#  EDITAR
# ------------------------------------------------------------
def pgProveedorEditar(request, idProveedor):

    proveedor = get_object_or_404(Proveedor, idProveedor=idProveedor)

    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)

        if form.is_valid():
            form.save()
            return redirect('provedor:indexProveedor')

    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, 'provedor/editar.html', {'form': form})


# ------------------------------------------------------------
#  ELIMINAR (LÓGICA)
# ------------------------------------------------------------
def pgProveedorEliminar(request, idProveedor):

    proveedor = get_object_or_404(Proveedor, idProveedor=idProveedor)
    proveedor.is_active = False
    proveedor.save()

    return redirect('provedor:indexProveedor')


# ------------------------------------------------------------
#  BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarProveedor(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    print("pagina:", page)
    proveedores = Proveedor.objects.filter(is_active=True)

    if filtro == 'nombre':
        print("Buscando por nombre")
        proveedores = proveedores.filter(nombre_proveedor__icontains=dato).order_by('nombre_proveedor')

    elif filtro == 'correo':
        proveedores = proveedores.filter(correo_electronico__icontains=dato).order_by('correo_electronico')

    elif filtro == 'tipo':
        proveedores = proveedores.filter(tipo_insumo__icontains=dato).order_by('tipo_insumo')

    else:
        proveedores = proveedores.order_by('idProveedor')

    paginator = Paginator(proveedores, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string('provedor/tabla_resultados.html', {
        'proveedores': page_obj.object_list
    })

    paginacion = render_to_string('provedor/paginacion.html', {
        'page_obj': page_obj
    })

    return JsonResponse({'tabla': tabla, 'paginacion': paginacion})
