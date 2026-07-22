from django import forms
from .models import LoteAnimales

class LoteAnimalesForm(forms.ModelForm):

    class Meta:
        model = LoteAnimales
        fields = [
            'especie',
            'cantidad_animales',
            'genero',                  
            'peso_ingreso',            
            'condicion_experimental', 
            'estado',                 
            'cepa',                    
            'fecha_baja',
            'fecha_ingreso',
            'tratamiento',
            'usuario',                 
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
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del tratamiento...'}),

            'fecha_baja': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

        }
