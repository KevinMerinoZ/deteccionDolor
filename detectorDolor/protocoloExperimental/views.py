from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import ProtocoloExperimental
from .forms import ProtocoloExperimentalForm


# ------------------------------------------------------------
#  INDEX
# ------------------------------------------------------------
def pgProtocoloIndex(request):

    protocolos = ProtocoloExperimental.objects.filter(
        is_active=True
    ).order_by('idprotocolosExperimentales')

    paginator = Paginator(protocolos, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'protocolos': page_obj.object_list,
    }
    return render(request, 'protocolo/index.html', context)


# ------------------------------------------------------------
#  CREAR
# ------------------------------------------------------------
def pgProtocoloCrear(request):

    if request.method == 'POST':
        form = ProtocoloExperimentalForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('protocoloExperimental:indexProtocolo')

    else:
        form = ProtocoloExperimentalForm()

    return render(request, 'protocolo/crear.html', {'form': form})


# ------------------------------------------------------------
#  EDITAR
# ------------------------------------------------------------
def pgProtocoloEditar(request, idProtocolo):

    protocolo = get_object_or_404(
        ProtocoloExperimental,
        idprotocolosExperimentales=idProtocolo
    )

    if request.method == 'POST':
        form = ProtocoloExperimentalForm(request.POST, instance=protocolo)

        if form.is_valid():
            form.save()
            return redirect('protocoloExperimental:indexProtocolo')

    else:
        form = ProtocoloExperimentalForm(instance=protocolo)

    return render(request, 'protocolo/editar.html', {'form': form})


# ------------------------------------------------------------
#  ELIMINAR (LÓGICA)
# ------------------------------------------------------------
def pgProtocoloEliminar(request, idProtocolo):

    protocolo = get_object_or_404(
        ProtocoloExperimental,
        idprotocolosExperimentales=idProtocolo
    )

    protocolo.is_active = False
    protocolo.save()

    return redirect('protocoloExperimental:indexProtocolo')


# ------------------------------------------------------------
#  BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarProtocolo(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    protocolos = ProtocoloExperimental.objects.filter(is_active=True)

    if filtro == 'nombre':
        protocolos = protocolos.filter(
            nombre_protocolo__icontains=dato
        ).order_by('nombre_protocolo')

    elif filtro == 'sustanciaExperimental':
        protocolos = protocolos.filter(sustancia_experimental_id__nombre_sustancia__icontains=dato).order_by('sustancia_experimental_id__nombre_sustancia')

    else:
        protocolos = protocolos.order_by('idprotocolosExperimentales')

    paginator = Paginator(protocolos, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string('protocolo/tabla_resultados.html', {
        'protocolos': page_obj.object_list
    })

    paginacion = render_to_string('protocolo/paginacion.html', {
        'page_obj': page_obj
    })

    return JsonResponse({
        'tabla': tabla,
        'paginacion': paginacion
    })
