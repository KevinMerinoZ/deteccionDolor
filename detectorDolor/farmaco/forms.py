from django import forms
from .models import Farmaco

class FarmacoForm(forms.ModelForm):
    class Meta:
        model = Farmaco
        fields = [
            'nombre',
            'presentacion',
            'tipo_farmaco',
            'fecha_llegada',
            'fecha_abierto',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Ketamina'}),
            'presentacion': forms.Select(attrs={'class': 'form-control'}),
            'tipo_farmaco': forms.Select(attrs={'class': 'form-control'}),
            'fecha_llegada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_abierto': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
