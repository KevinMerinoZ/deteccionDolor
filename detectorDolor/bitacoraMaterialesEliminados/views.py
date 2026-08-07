from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import F
from .forms import BitacoraMaterialesEliminadosForm
from .models import BitacoraMaterialesEliminados
from material.models import Material

# ----------------------------------------------------------------------
# Vista del listado de materiales eliminados
# ----------------------------------------------------------------------
def pgbitacoraMaterialesIndex(request):
    bitacoraMaterialesEliminados = (
        BitacoraMaterialesEliminados.objects
        .select_related(
            "material",
            "usuario_responsable"
        )
        .order_by("-fecha_registro")
    )

    return render(
        request,
        "bitacoraMateriales/index.html",
        {
            "bitacoraMaterialesEliminados": bitacoraMaterialesEliminados
        }
    )

# ----------------------------------------------------------------------
# Crear un material eliminado
# ----------------------------------------------------------------------
def pgbitacoraMaterialesCrear(request):
    if request.method == "POST":

        form = BitacoraMaterialesEliminadosForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                Material.objects.filter(pk=form.cleaned_data['material'].pk).update(piezas_disponibles=F('piezas_disponibles') - form.cleaned_data['cantidad'])

                form.save()

            messages.success(
                request,
                "Registro creado correctamente."
            )

            return redirect(
                "bitacoraMaterialesEliminados:index_materiales_eliminados"
            )

    else:

        form = BitacoraMaterialesEliminadosForm()

    return render(
        request,
        "bitacoraMateriales/crear.html",
        {
            "form": form
        }
    )
# ----------------------------------------------------------------------
# Editar material eliminado
# ----------------------------------------------------------------------
def pgbitacoraMaterialesEditar(request, id):

    registro = get_object_or_404(
        BitacoraMaterialesEliminados,
        pk=id
    )


    if request.method == "GET":
        form = BitacoraMaterialesEliminadosForm(
            instance=registro
        )

    print("entro a la función: ", registro.cantidad)

    if request.method == "POST":
        form = BitacoraMaterialesEliminadosForm(
            request.POST,
        )
        print("entro a la función")

        if form.is_valid():
            material_original = registro.material
            cantidad_original = registro.cantidad
            with transaction.atomic():
                nuevo_registro = form.save(commit=False)

                if material_original.pk == nuevo_registro.material.pk:

                    print("id cantidad original: ", cantidad_original)
                    print("nueva cantidad: ", nuevo_registro.cantidad)
                    Material.objects.filter(
                        pk=material_original.pk
                    ).update(
                        piezas_disponibles=F("piezas_disponibles") + cantidad_original - nuevo_registro.cantidad,
                    )
                    print("Se actualizó el mismo material, ajustando la cantidad disponible.")

                else:

                    Material.objects.filter(
                        pk=material_original.pk
                    ).update(
                        piezas_disponibles=F("piezas_disponibles") + cantidad_original
                    )

                    Material.objects.filter(
                        pk=nuevo_registro.material.pk
                    ).update(
                        piezas_disponibles=F("piezas_disponibles") - nuevo_registro.cantidad
                    )

                registro.material = nuevo_registro.material
                registro.cantidad = nuevo_registro.cantidad
                registro.fecha_eliminacion = nuevo_registro.fecha_eliminacion
                registro.motivo = nuevo_registro.motivo
                registro.usuario_responsable = nuevo_registro.usuario_responsable
                registro.observaciones = nuevo_registro.observaciones
                registro.save()

            messages.success(
                request,
                "Registro actualizado correctamente."
            )

            return redirect(
                "bitacoraMaterialesEliminados:index_materiales_eliminados"
            )

    return render(
        request,
        "bitacoraMateriales/editar.html",
        {
            "form": form,
            "registro": registro
        }
    )


# ----------------------------------------------------------------------
# Eliminar material eliminado
# ----------------------------------------------------------------------
def pgbitacoraMaterialesEliminar(request, id):

    registro = get_object_or_404(
        BitacoraMaterialesEliminados,
        pk=id
    )


    with transaction.atomic():
        Material.objects.filter(pk=registro.material.pk).update(piezas_disponibles=F('piezas_disponibles') + registro.cantidad)
        registro.delete()

    messages.success(
        request,
        "Registro eliminado correctamente."
    )

    return redirect(
        "bitacoraMaterialesEliminados:index_materiales_eliminados"
    )

# ----------------------------------------------------------------------
# Búsqueda y paginación AJAX
# ----------------------------------------------------------------------
def buscarMaterialesEliminados(request):

    dato = request.GET.get("dato", "")
    filtro = request.GET.get("tipoDato", "")
    page_number = request.GET.get("page", 1)

    registros = (
        BitacoraMaterialesEliminados.objects
        .select_related(
            "material",
            "usuario_responsable"
        )
    )

    if filtro == "material":

        registros = registros.filter(
            material__nombre__icontains=dato
        )

    elif filtro == "usuario_responsable":

        registros = registros.filter(
            usuario_responsable__nombre__icontains=dato
        )

    registros = registros.order_by("-fecha_registro")

    paginator = Paginator(registros, 10)

    page_obj = paginator.get_page(page_number)

    tabla_html = render_to_string(
        "bitacoraMateriales/tabla_resultados.html",
        {
            "bitacoraMaterialesEliminados": page_obj
        },
        request=request
    )

    paginacion_html = render_to_string(
        "bitacoraMateriales/paginacion.html",
        {
            "page_obj": page_obj
        },
        request=request
    )

    return JsonResponse({
        "tabla": tabla_html,
        "paginacion": paginacion_html,
    })
