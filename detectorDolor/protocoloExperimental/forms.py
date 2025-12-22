from django import forms
from .models import ProtocoloExperimental

class ProtocoloExperimentalForm(forms.ModelForm):

    class Meta:
        model = ProtocoloExperimental
        fields = [
            'nombre_protocolo',
            'objetivo_protocolo',
            'sustancia_experimental',
            'descripcion_protocolo',
            'consideraciones_eticas',
        ]

        widgets = {
            'nombre_protocolo': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'objetivo_protocolo': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'sustancia_experimental': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion_protocolo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'consideraciones_eticas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
