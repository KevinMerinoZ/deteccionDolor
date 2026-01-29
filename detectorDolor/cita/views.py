from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Cita
from usuario.models import Usuario
from .forms import CitaForm


# ------------------------------------------------------------
#  INDEX
# ------------------------------------------------------------
def pgCitaIndex(request):

    citas = Cita.objects.filter(is_active=True).order_by('-fecha', '-hora')

    paginator = Paginator(citas, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'citas': page_obj.object_list,
    }

    return render(request, 'cita/index.html', context)


# ------------------------------------------------------------
#  CREAR
# ------------------------------------------------------------
def pgCitaCrear(request):
    if request.method == 'POST':
        form = CitaForm(request.POST, user = request.user)

        if form.is_valid():
            cita = form.save(commit=False)

            # Usuario normal
            if not request.user.groups.filter(name='administrador').exists():
                cita.usuario = request.user.usuario  # o request.user si es FK directo

            cita.save()
            return redirect('cita:indexCita')
    else:
        form = CitaForm(user = request.user)

    return render(request, 'cita/crear.html', {'form': form})


# ------------------------------------------------------------
#  EDITAR
# ------------------------------------------------------------
def pgCitaEditar(request, idcitas):

    cita = get_object_or_404(Cita, idcitas=idcitas, is_active=True)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita, user = request.user)

        if form.is_valid():
            form.save()
            return redirect('cita:indexCita')
    else:
        form = CitaForm(instance=cita, user = request.user)

    return render(request, 'cita/editar.html', {'form': form})


# ------------------------------------------------------------
#  ELIMINAR (LÓGICA)
# ------------------------------------------------------------
def pgCitaEliminar(request, idcitas):

    cita = get_object_or_404(Cita, idcitas=idcitas)
    cita.is_active = False
    cita.save()

    return redirect('cita:indexCita')

def cambiarEstadoCita(request, idcitas, nuevo_estado):
    cita = get_object_or_404(Cita, idcitas=idcitas)

    if nuevo_estado in dict(Cita.ESTADOS).keys():
        cita.estado = nuevo_estado
        cita.save()

    return redirect('cita:indexCita')

# ------------------------------------------------------------
#  BÚSQUEDA DINÁMICA (AJAX)
# ------------------------------------------------------------
def buscarCita(request):

    dato = request.GET.get('dato', '')
    filtro = request.GET.get('tipoDato', '')
    page = request.GET.get('page', 1)

    es_admin = request.user.groups.filter(name='administrador').exists()

    if request.user.groups.first().name == 'administrador':
        citas = Cita.objects.filter(is_active=True)
    else:
        usuarioAct = request.user
        citas = Cita.objects.filter(is_active=True, usuario_id__user__username=usuarioAct)

    if filtro == 'usuario':
        citas = citas.filter(
            usuario__nombre__icontains=dato
        ).order_by('usuario__nombre')

    elif filtro == 'protocolo':
        citas = citas.filter(
            protocolo_experimental__nombre_protocolo__icontains=dato
        ).order_by('protocolo_experimental__nombre_protocolo')

    elif filtro == 'fecha':
        citas = citas.filter(fecha__icontains=dato).order_by('fecha')

    else:
        citas = citas.order_by('-fecha', '-hora')

    paginator = Paginator(citas, 10)
    page_obj = paginator.get_page(page)

    tabla = render_to_string('cita/tabla_resultados.html', {
        'citas': page_obj.object_list,
        'es_administrador': es_admin
    })

    paginacion = render_to_string('cita/paginacion.html', {
        'page_obj': page_obj
    })

    return JsonResponse({
        'tabla': tabla,
        'paginacion': paginacion
    })
