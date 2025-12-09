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
            'observaciones',
            'usuario',                 # ← agregado
        ]

        widgets = {
            'genero': forms.Select(attrs={'class': 'form-select'}),  
            'condicion_experimental': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'cepa': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),

            'peso_ingreso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad_animales': forms.NumberInput(attrs={'class': 'form-control'}),

            'fecha_baja': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
