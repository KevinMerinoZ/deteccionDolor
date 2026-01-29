from django import forms
from .models import SesionExperimental
from datetime import date, timedelta


class SesionExperimentalForm(forms.ModelForm):

    class Meta:
        model = SesionExperimental
        fields = [
            'fecha',
            'nombre_experimento',
            'farmaco',
            'usuario',
            'protocolo_experimental',
            'noMediciones1',
            'intervaloTemp1',
            'noMediciones2',
            'intervaloTemp2',
            'observaciones',
        ]

        widgets = {
            'farmaco': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'protocolo_experimental': forms.Select(attrs={'class': 'form-select'}),

            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'nombre_experimento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experimento X'}),
            
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    
            'noMediciones1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10'}),
            'intervaloTemp1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5'}),
            'noMediciones2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '12'}),
            'intervaloTemp2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10'}),
        }
    
    def __init__ (self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not user.groups.filter(name='administrador').exists():
            self.fields.pop('usuario')
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha is None:
            raise forms.ValidationError("La fecha es obligatoria.")
        # elif fecha 
        return fecha
