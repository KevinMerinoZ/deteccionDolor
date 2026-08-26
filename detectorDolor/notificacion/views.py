from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from usuario.models import Usuario

# Create your views here.

def obtener_notificaciones(request):
    """
    Descripción:
        Consulta las notificaciones activas para el usuario autenticado.

    Entradas:
        request (HttpRequest): Solicitud del navegador.

    Salidas:
        JsonResponse: Lista de notificaciones en formato JSON.
    """
    if request.user.is_authenticated:
        usuario = get_object_or_404(Usuario, user=request.user)
        notificaciones = usuario.notificaciones.filter().values('idNotificaciones', 'titulo', 'mensaje', 'fecha_creacion', 'leido').order_by('-fecha_creacion')

        notificacionesNoLeidas = notificaciones.filter(leido=False).count()
        contenedor = render_to_string('layouts/contNotificaciones.html', {
            'notificaciones': notificaciones,
            'notificacionesNoLeidas': notificacionesNoLeidas,
        })
        return JsonResponse({'contenedor': contenedor}, safe=False)
    else:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
    
def actualizar_estado_notificacion(request, id):
    """
    Descripción:
        Marca una notificación como leída.

    Entradas:
        request (HttpRequest): Solicitud del navegador.
        id (int): ID de la notificación a actualizar.

    Salidas:
        JsonResponse: Estado de la operación.
    """
    if request.user.is_authenticated:
        usuario = get_object_or_404(Usuario, user=request.user)
        notificacion = usuario.notificaciones.filter(idNotificaciones=id).first()

        if notificacion:
            notificacion.leido = True
            notificacion.save()
            notificacionesNoLeidas = usuario.notificaciones.filter(leido=False).count()
            return JsonResponse({'success': 'Notificación marcada como leída', 'notificacionesNoLeidas': notificacionesNoLeidas})
        else:
            return JsonResponse({'error': 'Notificación no encontrada'}, status=404)
    else:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
    
def eliminar_notificacion(request, id):
    """
    Descripción:
        Elimina una notificación del sistema.

    Entradas:
        request (HttpRequest): Solicitud del navegador.
        id (int): ID de la notificación a eliminar.

    Salidas:
        JsonResponse: Estado de la operación.
    """
    if request.user.is_authenticated:
        usuario = get_object_or_404(Usuario, user=request.user)
        notificacion = usuario.notificaciones.filter(idNotificaciones=id).first()

        if notificacion:
            notificacion.delete()
            notificacionesNoLeidas = usuario.notificaciones.filter(leido=False).count()
            return JsonResponse({'success': 'Notificación eliminada', 'notificacionesNoLeidas': notificacionesNoLeidas, 'idEliminada': id})
        else:
            return JsonResponse({'error': 'Notificación no encontrada'}, status=404)
    else:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)