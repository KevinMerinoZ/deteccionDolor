from django import forms
from .models import SustanciaExperimental


class SustanciaExperimentalForm(forms.ModelForm):

    class Meta:
        model = SustanciaExperimental
        fields = [
            'nombre_sustancia',
            'tipo',
            'consentracion',
            'presentacion',
            'unidad_medida',
            'proveedor',
        ]

        widgets = {
            'nombre_sustancia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solución salina'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'consentracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '100mg/200ml'}),
            
            'presentacion': forms.Select(attrs={'class': 'form-select'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
        }
