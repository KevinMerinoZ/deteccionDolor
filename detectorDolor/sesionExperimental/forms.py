from django import forms
from .models import SesionExperimental


class SesionExperimentalForm(forms.ModelForm):

    class Meta:
        model = SesionExperimental
        fields = [
            'fecha',
            'nombre_experimento',
            'farmaco',
            'usuario',
            'protocolo_experimental',
            'numero_mediciones',
            'observaciones',
        ]

        widgets = {
            'fecha': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'nombre_experimento': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'farmaco': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'usuario': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'protocolo_experimental': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'numero_mediciones': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
