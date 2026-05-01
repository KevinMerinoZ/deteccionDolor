from django import forms
from .models import Cita
from usuario.models import Usuario


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            'fechaInicio',
            'fechaFin',
            'sala_laboratorio',
            'usuario',
            'protocolo_experimental',
        ]

        widgets = {
            'fechaInicio': forms.DateTimeInput(format=('%Y-%m-%d %H:%M'), attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fechaFin': forms.DateTimeInput(format=('%Y-%m-%d %H:%M'), attrs={'class': 'form-control', 'type': 'datetime-local'}),

            'sala_laboratorio': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'protocolo_experimental': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sala_laboratorio'].queryset = self.fields['sala_laboratorio'].queryset.filter(is_active=True).order_by('nombre')
        self.fields['protocolo_experimental'].queryset = self.fields['protocolo_experimental'].queryset.filter(is_active=True).order_by('nombre_protocolo')

        self.fields['usuario'].queryset = Usuario.objects.filter(is_active=True).order_by('user__username')
        self.fields["usuario"].label_from_instance = lambda obj: obj.user.username

        # Esto asegura que el valor se formatee correctamente al cargar el formulario
        if not user.groups.filter(name='administrador').exists():
            self.fields.pop('usuario')
            
        if self.instance and self.instance.pk:
            if self.instance.fechaInicio:
                self.initial['fechaInicio'] = self.instance.fechaInicio.strftime('%Y-%m-%d %H:%M')
            if self.instance.fechaFin:
                self.initial['fechaFin'] = self.instance.fechaFin.strftime('%Y-%m-%d %H:%M')
