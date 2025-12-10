from django import forms
from .models import Farmaco

class FarmacoForm(forms.ModelForm):
    class Meta:
        model = Farmaco
        fields = [
            'nombre',
            'presentacion',
            'tipo_farmaco',
            'via_administracion',
            'consentracion',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'presentacion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_farmaco': forms.TextInput(attrs={'class': 'form-control'}),
            'via_administracion': forms.TextInput(attrs={'class': 'form-control'}),
            'consentracion': forms.TextInput(attrs={'class': 'form-control'}),
        }
