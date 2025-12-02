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

# Create your views here.
def pgPrincipal(request):
    return render(request, 'paginas/principal.html')

def pgUsuariosIndex(request):
    usuarios = Usuario.objects.select_related('user').all()
    return render(request, 'usuarios/index.html', {'usuarios': usuarios})

def pgUsuariosCrear(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.cleaned_data['matricula'] = form.cleaned_data['matricula'].lower()
                    contr = generar_password()

                    user = User.objects.create(
                        username=form.cleaned_data['matricula'],
                        password=make_password(contr),
                    )

                    grupo = Group.objects.get(name=form.cleaned_data['tipo_usuario'])
                    user.groups.add(grupo)

                    usuario = form.save(commit=False)
                    usuario.user = user
                    usuario.fecha_registro = date.today()
                    usuario.save()

                    messages.success(request, "Usuario creado correctamente.")

                    enviarCorreo(usuario.nombre, usuario.matricula, usuario.correo, contr, 'Registro de Usuario', 'Tu cuenta ha sido creada exitosamente.')

                    return redirect('index')

            except Exception as e:
                print(e)
                messages.error(request, "No se pudo crear el usuario.")
                return redirect('crear')

        else:
            messages.error(request, "Formulario inválido. Por favor, corrige los errores.")

    else:
        form = UsuarioForm()

    return render(request, 'usuarios/crear.html', {'form': form})


def enviarCorreo(name: str, matricula: str, email: str, password: str,encabezado: str, message: str):
    template = render_to_string('email/email_template.html',{
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

def generar_password(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def pgUsuariosEditar(request, id):
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
                    return redirect('index')

            except Exception as e:
                print(e)
                messages.error(request, "No se pudo actualizar el usuario.")

        else:
            messages.error(request, "Formulario inválido.")

    return render(request, 'usuarios/editar.html', {
        'form': form,
        'usuario': usuario
    })

def pgUsuariosEliminar(request, id):
    usuario = get_object_or_404(User, id=id)

    try:
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
    except Exception as e:
        messages.error(request, "No se pudo eliminar el usuario.")

    return redirect('index')

def buscar_usuarios(request):
    dato = request.GET.get('dato', '')
    page_number = request.GET.get('page', 1)
    tipoDato = request.GET.get('tipoDato', '')


    if tipoDato == 'nombre':
        usuarios = Usuario.objects.filter(nombre__icontains=dato).order_by('nombre')
    elif tipoDato == 'apellidoP':
        usuarios = Usuario.objects.filter(apellido_paterno__icontains=dato).order_by('apellido_paterno')
    elif tipoDato == 'matricula':
        usuarios = Usuario.objects.filter(matricula__icontains=dato).order_by('matricula')
    elif tipoDato == 'correo':
        usuarios = Usuario.objects.filter(correo__icontains=dato).order_by('correo')
    else:
        usuarios = Usuario.objects.all().order_by('idUsuarios')

    # Paginación (10 por página)
    paginator = Paginator(usuarios, 10)
    page_obj = paginator.get_page(page_number)

    # Renderizamos SOLO la tabla
    tabla_html = render_to_string('usuarios/tabla_resultados.html', {
        'usuarios': page_obj,
    })

    # Renderizamos SOLO los botones de paginación
    paginacion_html = render_to_string('usuarios/paginacion.html', {
        'page_obj': page_obj,
    })

    return JsonResponse({
        'tabla': tabla_html,
        'paginacion': paginacion_html,
    })