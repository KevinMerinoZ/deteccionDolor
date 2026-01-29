from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import date

from .models import LoteAnimales
from .forms import LoteAnimalesForm


# ----------------------------------------------------------------------
# Listado principal
# ----------------------------------------------------------------------
def pgLotesIndex(request):
    """
    Descripción:
        Muestra la lista de lotes de animales registrados. Permite
        filtrar por especie, estado y rango de fechas.

    Entradas:
        request (HttpRequest): Solicitud del navegador.

    Salidas:
        HttpResponse: Render de la plantilla index.html con los lotes.
    """

    especie = request.GET.get('especie', '')
    estado = request.GET.get('estado', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    lotes = LoteAnimales.objects.filter(is_active=True).order_by('-fecha_ingreso')

    if especie:
        lotes = lotes.filter(especie__icontains=especie)

    if estado:
        lotes = lotes.filter(estado__icontains=estado)

    if fecha_inicio and fecha_fin:
        lotes = lotes.filter(fecha_ingreso__range=[fecha_inicio, fecha_fin])

    return render(request, 'lotesAnimales/index.html', {
        'lotes': lotes
    })


# ----------------------------------------------------------------------
# Crear lote
# ----------------------------------------------------------------------
def pgLotesCrear(request):
    """
    Descripción:
        Permite registrar un nuevo lote de animales. La fecha de ingreso
        se asigna automáticamente.

    Entradas:
        request (HttpRequest): Datos del formulario vía POST.

    Salidas:
        HttpResponse: Render del formulario o redirect al listado.
    """

    if request.method == 'POST':
        form = LoteAnimalesForm(request.POST)

        print(form.errors)
        if form.is_valid():
            lote = form.save(commit=False)
            lote.fecha_ingreso = date.today()
            lote.save()
            messages.success(request, "Lote registrado correctamente.")
            return redirect('lotesAnimales:indexLotes')
        else:
            messages.error(request, "Formulario inválido.")

    else:
        form = LoteAnimalesForm()

    return render(request, 'lotesAnimales/crear.html', {'form': form})


# ----------------------------------------------------------------------
# Editar lote
# ----------------------------------------------------------------------
def pgLotesEditar(request, id):
    """
    Descripción:
        Permite modificar un lote ya registrado.

    Entradas:
        request (HttpRequest)
        id (int): ID del lote a editar.

    Salidas:
        HttpResponse: Render del formulario o redirect.
    """

    lote = get_object_or_404(LoteAnimales, idlotesAnimales=id)
    form = LoteAnimalesForm(request.POST or None, instance=lote)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Lote actualizado correctamente.")
            return redirect('lotesAnimales:indexLotes')
        else:
            messages.error(request, "Formulario inválido.")

    return render(request, 'lotesAnimales/editar.html', {
        'form': form,
        'lote': lote
    })


# ----------------------------------------------------------------------
# Eliminar lote
# ----------------------------------------------------------------------
def pgLotesEliminar(request, id):
    """
    Descripción:
        Establece un lote como inactivo (borrado lógico).

    Entradas:
        request (HttpRequest)
        id (int): ID del lote

    Salidas:
        HttpResponse: Redirect al listado.
    """

    lote = get_object_or_404(LoteAnimales, idlotesAnimales=id)
    lote.is_active = False
    lote.save()
    messages.success(request, "Lote eliminado correctamente.")
    return redirect('lotesAnimales:indexLotes')


# ----------------------------------------------------------------------
# Dar de baja lote
# ----------------------------------------------------------------------
def pgLotesDarBaja(request, id):
    """
    Descripción:
        Permite dar de baja un lote de animales estableciendo la
        fecha de baja como la fecha actual.

    Entradas:
        request (HttpRequest)
        id (int): ID del lote a dar de baja.

    Salidas:
        HttpResponse: Redirect al listado.
    """

    lote = get_object_or_404(LoteAnimales, idlotesAnimales=id)

    if lote.fecha_baja is None:
        lote.fecha_baja = date.today()
        lote.save()
        messages.success(request, "Lote dado de baja correctamente.")
    else:
        messages.warning(request, "El lote ya ha sido dado de baja.")

    return redirect('lotesAnimales:indexLotes')

# ----------------------------------------------------------------------
# Búsqueda dinámica AJAX
# ----------------------------------------------------------------------
def buscar_lotes(request):
    """
    Descripción:
        Realiza búsqueda dinámica por especie, estado o número de lote.
        Devuelve HTML parcial para reemplazar tabla y paginación.

    Entradas:
        request (HttpRequest)

    Salidas:
        JsonResponse: Contiene HTML parcial.
    """

    dato = request.GET.get('dato', '')
    page_number = request.GET.get('page', 1)
    tipoDato = request.GET.get('tipoDato', '')

    if tipoDato == 'especie':
        lotes = LoteAnimales.objects.filter(especie__icontains=dato, is_active=True).order_by('especie')
    elif tipoDato == 'estado':
        lotes = LoteAnimales.objects.filter(estado__icontains=dato, is_active=True).order_by('estado')  
    elif tipoDato == 'responsable':
        lotes = LoteAnimales.objects.select_related('usuario').filter(usuario__nombre__icontains=dato, is_active=True).order_by('usuario__nombre') 
    else:
        lotes = LoteAnimales.objects.filter(is_active=True)

    paginator = Paginator(lotes, 10)
    page_obj = paginator.get_page(page_number)
    print(page_obj)

    tabla_html = render_to_string('lotesAnimales/tabla_resultados.html', {
        'lotes': page_obj,
    })

    paginacion_html = render_to_string('lotesAnimales/paginacion.html', {
        'page_obj': page_obj,
    })

    return JsonResponse({
        'tabla': tabla_html,
        'paginacion': paginacion_html,
    })
