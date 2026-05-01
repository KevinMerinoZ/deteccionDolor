from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import date
from django.db import transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import UsuarioForm
from django.contrib.auth.decorators import user_passes_test
from .models import Usuario
from sesionExperimental.models import SesionExperimental
from django.db.models import Count
from django.utils import timezone

import io
import xlsxwriter
import secrets
import string

# ----------------------------------------------------------------------
# Vista principal del panel
# ----------------------------------------------------------------------
def pgPrincipal(request):
    """
    Descripción:
        Renderiza la página principal del sistema.

    Entradas:
        request (HttpRequest): Solicitud del navegador.

    Salidas:
        HttpResponse: Render de la plantilla principal.html.
    """
    return render(request, 'paginas/principal.html')


# ----------------------------------------------------------------------
# Vista del listado de usuarios
# ----------------------------------------------------------------------
def pgUsuariosIndex(request):
    """
    Descripción:
        Muestra la lista completa de usuarios registrados.

    Entradas:
        request (HttpRequest): Solicitud del navegador.

    Salidas:
        HttpResponse: Render de la plantilla index.html con los usuarios.
    """
    usuarios = Usuario.objects.select_related('user').filter(is_active=True).order_by('idUsuarios')
    return render(request, 'usuarios/index.html', {'usuarios': usuarios})


# ----------------------------------------------------------------------
# Crear un usuario
# ----------------------------------------------------------------------
def pgUsuariosCrear(request):
    """
    Descripción:
        Permite registrar un nuevo usuario, creando tanto el protocolo User
        como el protocolo Usuario asociado. Envía correo de creación.

    Entradas:
        request (HttpRequest): Datos del formulario vía POST.

    Salidas:
        HttpResponse: Render del formulario o redirect al listado.
    """
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.cleaned_data['matricula'] = form.cleaned_data['matricula'].lower()
                    contr = generar_password()

                    # Crear usuario base
                    user = User.objects.create(
                        username=form.cleaned_data['matricula'],
                        password=make_password(contr),
                    )

                    # Asignar grupo
                    grupo = Group.objects.get(name=form.cleaned_data['tipo_usuario'])
                    user.groups.add(grupo)

                    # Crear protocolo Usuario
                    usuario = form.save(commit=False)
                    usuario.user = user
                    usuario.fecha_registro = date.today()
                    usuario.save()

                    messages.success(request, "Usuario creado correctamente.")

                    enviarCorreo(usuario.nombre, usuario.matricula, usuario.correo, contr, 'Registro de Usuario', 'Tu cuenta ha sido creada exitosamente.')

                    return redirect('usuario:indexUsuario')

            except Exception as e:
                print(e)
                messages.error(request, "No se pudo crear el usuario.")
                return redirect('usuario:crearUsuario')

        else:
            messages.error(request, "Formulario inválido. Por favor, corrige los errores.")

    else:
        form = UsuarioForm()

    return render(request, 'usuarios/crear.html', {'form': form})


# ----------------------------------------------------------------------
# Enviar correo
# ----------------------------------------------------------------------
def enviarCorreo(name: str, matricula: str, email: str, password: str, encabezado: str, message: str):
    """
    Descripción:
        Envía un correo electrónico al usuario con un mensaje personalizado.

    Entradas:
        name (str): Nombre del destinatario.
        matricula (str): Matrícula del usuario.
        email (str): Correo del destinatario.
        password (str): Contraseña generada.
        encabezado (str): Asunto del correo.
        message (str): Mensaje del cuerpo.

    Salidas:
        None: Solo envía el correo.
    """
    template = render_to_string('email/email_template.html', {
        'nombre': name,
        'matricula': matricula,
        'pass': password,
        'mensaje': message,
    })

    correoElectronico = EmailMultiAlternatives(
        subject=encabezado,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )

    correoElectronico.attach_alternative(template, 'text/html')
    correoElectronico.send()


# ----------------------------------------------------------------------
# Generar contraseña aleatoria
# ----------------------------------------------------------------------
def generar_password(longitud=12):
    """
    Descripción:
        Genera una contraseña aleatoria segura utilizando letras,
        números y símbolos.

    Entradas:
        longitud (int): Longitud deseada de la contraseña (default=12).

    Salidas:
        str: Cadena generada como contraseña.
    """
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))


# ----------------------------------------------------------------------
# Editar usuario
# ----------------------------------------------------------------------
def pgUsuariosEditar(request, id):
    """
    Descripción:
        Permite editar los datos de un usuario existente, incluyendo su
        matrícula, tipo de usuario y datos personales.

    Entradas:
        request (HttpRequest): Solicitud del navegador.
        id (int): ID del usuario a editar.

    Salidas:
        HttpResponse: Render del formulario o redirect al listado.
    """
    usuario = get_object_or_404(Usuario, idUsuarios=id)
    form = UsuarioForm(request.POST or None, instance=usuario)

    if request.method == 'POST':
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.cleaned_data['matricula'] = form.cleaned_data['matricula'].lower()
                    usuario = form.save(commit=False)

                    usuario.user.username = form.cleaned_data['matricula']

                    nuevo_grupo = form.cleaned_data['tipo_usuario']
                    usuario.user.groups.clear()
                    grupo = Group.objects.get(name=nuevo_grupo)
                    usuario.user.groups.add(grupo)

                    usuario.user.save()
                    usuario.save()

                    messages.success(request, "Usuario actualizado correctamente.")
                    return redirect('usuario:indexUsuario')

            except Exception as e:
                print(e)
                messages.error(request, "No se pudo actualizar el usuario.")

        else:
            messages.error(request, "Formulario inválido.")

    return render(request, 'usuarios/editar.html', {
        'form': form,
        'usuario': usuario
    })


# ----------------------------------------------------------------------
# Eliminar usuario
# ----------------------------------------------------------------------
def pgUsuariosEliminar(request, id):
    """
    Descripción:
        Elimina un usuario del sistema utilizando su ID.

    Entradas:
        request (HttpRequest): Solicitud del navegador.
        id (int): ID del usuario del protocolo User.

    Salidas:
        HttpResponse: Redirect al listado de usuarios.
    """
    usuario = get_object_or_404(Usuario, idUsuarios=id)

    try:
        usuario.is_active = False
        usuario.user.is_active = False
        usuario.user.save()
        usuario.save()
        messages.success(request, "Usuario eliminado correctamente.")
    except Exception as e:
        messages.error(request, "No se pudo eliminar el usuario.")

    return redirect('usuario:indexUsuario')

# ----------------------------------------------------------------------
# Reporte de sesiones experimentales por usuario
# ----------------------------------------------------------------------
def reporteSesionesExp(request):
    usuarios = Usuario.objects.filter(is_active=True)
    if request.method == 'POST':
        usuario_username = request.POST.get('usuario')

        if not usuario_username:
            return HttpResponse("Debe proporcionar el usuario")

        try:
            usuario = usuarios.get(user__username=usuario_username)
        except Usuario.DoesNotExist:
            return HttpResponse("Usuario no encontrado")

        sesiones = SesionExperimental.objects.filter(usuario=usuario)

        total_sesiones = sesiones.count()

        finalizadas = sesiones.filter(estado=True).count()
        pendientes = sesiones.filter(estado=False).count()

        # Crear archivo en memoria
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Reporte")

        # FORMATOS
        titulo = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 16
        })

        encabezado = workbook.add_format({
            'bold': True,
            'align': 'center',
            'border': 1
        })

        celda = workbook.add_format({
            'border': 1,
            'align': 'center'
        })

        # Ajustar columnas
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 20)

        # Título
        worksheet.merge_range('A1:B1', 'Reporte de Sesiones Experimentales por Usuario', titulo)

        # Información del usuario
        worksheet.write('A3', 'Usuario:', encabezado)
        worksheet.write('B3', f"{usuario.nombre} {usuario.apellido_paterno}", celda)

        worksheet.write('A4', 'Total de sesiones:', encabezado)
        worksheet.write('B4', total_sesiones, celda)

        # Encabezados tabla
        worksheet.write('A6', 'Estado', encabezado)
        worksheet.write('B6', 'Cantidad', encabezado)

        # Datos
        worksheet.write('A7', 'Finalizadas', celda)
        worksheet.write('B7', finalizadas, celda)

        worksheet.write('A8', 'Pendientes', celda)
        worksheet.write('B8', pendientes, celda)

        # Crear gráfica
        chart = workbook.add_chart({'type': 'column'})

        chart.add_series({
            'name': 'Sesiones',
            'categories': '=Reporte!$A$7:$A$8',
            'values': '=Reporte!$B$7:$B$8',
            'data_labels': {'value': True},
        })

        chart.set_title({'name': 'Sesiones realizadas por estado'})
        chart.set_x_axis({'name': 'Estado'})
        chart.set_y_axis({'name': 'Cantidad de sesiones', 'major_unit':1})

        worksheet.insert_chart('D6', chart)

        workbook.close()
        output.seek(0)

        # Respuesta para descargar
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        nombreArchivo = f"reporte_sesiones_usuario_{usuario_username}_{timezone.now().strftime('%Y-%m-%d %H-%M-%S')}.xlsx"

        response['Content-Disposition'] = f'attachment; filename="{nombreArchivo}"'

        return response
    
    return render(request, 'usuarios/reporteSesionesExp.html', {'usuarios': usuarios})

# ----------------------------------------------------------------------
# Funciones de notificaciones
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# Búsqueda y paginación AJAX
# ----------------------------------------------------------------------
def buscar_usuarios(request):
    """
    Descripción:
        Busca usuarios por nombre, apellido, matrícula o correo.
        Devuelve tablas HTML y paginación mediante AJAX.

    Entradas:
        request (HttpRequest): Parámetros GET:
            - dato (str): Texto a buscar.
            - page (int): Número de página.
            - tipoDato (str): Tipo de filtro.

    Salidas:
        JsonResponse: Contiene HTML de la tabla y la paginación.
    """
    dato = request.GET.get('dato', '')
    page_number = request.GET.get('page', 1)
    tipoDato = request.GET.get('tipoDato', '')

    if tipoDato == 'nombre':
        usuarios = Usuario.objects.filter(nombre__icontains=dato, is_active=True).order_by('nombre')
    elif tipoDato == 'apellidoP':
        usuarios = Usuario.objects.filter(apellido_paterno__icontains=dato, is_active=True).order_by('apellido_paterno')
    elif tipoDato == 'matricula':
        usuarios = Usuario.objects.filter(matricula__icontains=dato, is_active=True).order_by('matricula')
    elif tipoDato == 'correo':
        usuarios = Usuario.objects.filter(correo__icontains=dato, is_active=True).order_by('correo')
    else:
        usuarios = Usuario.objects.filter(is_active=True).order_by('idUsuarios')

    paginator = Paginator(usuarios, 10)
    page_obj = paginator.get_page(page_number)

    tabla_html = render_to_string('usuarios/tabla_resultados.html', {
        'usuarios': page_obj,
    })

    paginacion_html = render_to_string('usuarios/paginacion.html', {
        'page_obj': page_obj,
    })

    return JsonResponse({
        'tabla': tabla_html,
        'paginacion': paginacion_html,
    })
