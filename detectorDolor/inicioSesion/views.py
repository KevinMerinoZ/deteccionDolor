from datetime import timedelta
from django.utils import timezone
import secrets
import string
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import PassVerificacion
from usuario.models import Usuario
from django.contrib.auth.hashers import make_password

from django.conf import settings

import random
# from django.http import HttpResponse

# Create your views here.
def login_vista(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        else:
            login(request, user)
            return redirect('core:interfazPrincipal')
    else:
        if request.user.is_authenticated:
            return redirect('core:interfazPrincipal')

        
    return render(request, 'login.html')

def recuperarContrasena(request):
    if request.method == 'POST':
        if request.POST.get('btnEnviarCodigo') or request.POST.get('btnReenviar'):
            usuario = Usuario.objects.filter(correo=request.POST.get('email')).first()

            if not usuario:
                return render(request, 'recuperarContrasena.html', {'error': 'El correo electrónico no está registrado.'})

            codigo = f"{random.randint(0, 9999):04d}"

            PassVerificacion.objects.filter(user=usuario.user, usado=False).update(usado=True)

            PassVerificacion.objects.create(
                user=usuario.user,
                codigo=codigo,
                fechaExpiro=timezone.now() + timedelta(minutes=1)
            )
            
            email = request.POST.get('email')
            encabezado = 'Recuperación de contraseña'
            message = 'Código de recuperación de contraseña: ' + codigo

            enviarCorreo(email, encabezado, message)

            return render(request, 'recuperarContrasena.html', {'flag': True, 'email': email})
        
        if request.POST.get('btnVerificar'):
            codigoIngresado = request.POST.get('codigo')
            email = request.POST.get('email')

            usuario = Usuario.objects.filter(correo=email).first()

            reset = PassVerificacion.objects.filter(
                user=usuario.user,
                usado=False
            ).latest("fechaCreacion")

            if not reset or not reset.is_valid():
                return render(request, 'recuperarContrasena.html', {'error': 'El código ha expirado. Por favor, solicite un nuevo código.', 'flag': True, 'email': email})

            if reset.codigo != codigoIngresado:
                return render(request, 'recuperarContrasena.html', {'error': 'El código ingresado es incorrecto.', 'flag': True, 'email': email})
            
            reset.usado = True
            reset.save()

            nuevaContrasena = generar_password()
            usuario.user.set_password(nuevaContrasena)
            
            usuario.user.save()

            encabezado = 'Nueva contraseña'
            message = f'Su nueva contraseña es: {nuevaContrasena}'

            enviarCorreo(email, encabezado, message)

            return render(request, 'recuperarContrasena.html', {'success': 'Se ha enviado una nueva contraseña a su correo electrónico.'})

    return render(request, 'recuperarContrasena.html')


def enviarCorreo(email: str, encabezado: str, message: str):

    template = render_to_string('email/email_recuperar.html', {
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