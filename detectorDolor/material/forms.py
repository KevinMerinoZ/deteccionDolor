from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            'nombre',
            'material_fabricacion',
            'piezas_disponibles',
            'uso',
            'proveedor',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'material_fabricacion': forms.TextInput(attrs={'class': 'form-control'}),
            'piezas_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
            'uso': forms.TextInput(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
        }
