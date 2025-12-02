from django import forms
from .models import Usuario
from django.core.validators import RegexValidator

class UsuarioForm(forms.ModelForm):

    matricula = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]{4}[0-9]{6}$',
                message="La matrícula debe tener 4 letras seguidas de 6 números."
            )
        ]
    )

    nombre = forms.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$',
                message="El nombre solo puede contener letras."
            )
        ]
    )

    apellido_paterno = forms.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$',
                message="El apellido solo puede contener letras."
            )
        ]
    )

    apellido_materno = forms.CharField(
        max_length=30,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$',
                message="El apellido materno solo puede contener letras."
            )
        ]
    )

    tipo_usuario = forms.ChoiceField(
        choices=[
            ('administrador', 'Administrador'),
            ('laboratorista', 'Laboratorista'),
            ('investigador', 'Investigador')
        ]
    )

    correo = forms.EmailField(
        max_length=100
    )

    class Meta:
        model = Usuario
        fields = [
            'matricula', 'nombre', 'apellido_paterno', 'apellido_materno',
            'tipo_usuario', 'correo'
        ]
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.matricula = usuario.matricula.lower()

        if commit:
            usuario.save()
        return usuario
