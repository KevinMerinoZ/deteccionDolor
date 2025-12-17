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
            'nombre_sustancia': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'tipo': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'consentracion': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'presentacion': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'unidad_medida': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'proveedor': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }
