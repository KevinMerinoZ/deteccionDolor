from django import forms
from .models import BitacoraMaterialesEliminados
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class BitacoraMaterialesEliminadosForm(forms.ModelForm):

    class Meta:
        model = BitacoraMaterialesEliminados
        fields = [
            'material',
            'cantidad',
            'fecha_eliminacion',
            'motivo',
            'usuario_responsable',
            'observaciones',                 
        ]

        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max':200}),
            'fecha_eliminacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Motivo de la eliminación...'}),
            'usuario_responsable': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones adicionales...'}),

            'fecha_baja': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

        }


    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 1 or cantidad > 200:
            raise ValidationError("La cantidad debe estar entre 1 y 200.",code='limite_cantidad')
        return cantidad

