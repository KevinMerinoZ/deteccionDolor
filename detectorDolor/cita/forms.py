from django import forms
from .models import Cita


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            'fecha',
            'hora',
            'usuario',
            'protocolo_experimental',
        ]

        widgets = {
            'fecha': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(format=('%H:%M'), attrs={'class': 'form-control', 'type': 'time'}),

            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'protocolo_experimental': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Esto asegura que el valor se formatee correctamente al cargar el formulario
        if not user.groups.filter(name='administrador').exists():
            self.fields.pop('usuario')
            
        if self.instance and self.instance.pk:
            if self.instance.fecha:
                self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%d')
            if self.instance.hora:
                self.initial['hora'] = self.instance.hora.strftime('%H:%M')
