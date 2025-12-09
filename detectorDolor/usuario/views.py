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
        Permite registrar un nuevo usuario, creando tanto el modelo User
        como el modelo Usuario asociado. Envía correo de creación.

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

                    # Crear modelo Usuario
                    usuario = form.save(commit=False)
                    usuario.user = user
                    usuario.fecha_registro = date.today()
                    usuario.save()

                    messages.success(request, "Usuario creado correctamente.")

                    enviarCorreo(usuario.nombre, usuario.matricula, usuario.correo, contr, 'Registro de Usuario', 'Tu cuenta ha sido creada exitosamente.')

                    return redirect('indexUsuario')

            except Exception as e:
                print(e)
                messages.error(request, "No se pudo crear el usuario.")
                return redirect('crearUsuario')

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
                    return redirect('indexUsuario')

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
        id (int): ID del usuario del modelo User.

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

    return redirect('indexUsuario')


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
