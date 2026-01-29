from django import forms
from .models import LoteAnimales

class LoteAnimalesForm(forms.ModelForm):

    class Meta:
        model = LoteAnimales
        fields = [
            'especie',
            'cantidad_animales',
            'genero',                   # ← agregado
            'peso_ingreso',            # ← agregado
            'condicion_experimental',  # ← agregado
            'estado',                  # ← agregado
            'cepa',                    # ← agregado
            'fecha_baja',
            'usuario',                 # ← agregado
        ]

        widgets = {
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),  
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),

            'cepa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wistar, CD-1, Sprague Dawley...'}),
            'condicion_experimental': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Control, estrés crónico, dolor inflamatorio...'}),

            'peso_ingreso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder':'15'}),
            'cantidad_animales': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '20'}),

            'fecha_baja': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

        }
