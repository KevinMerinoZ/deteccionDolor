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
            'cantidad_animales': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '20', 'min': '1', 'max': '30'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del tratamiento...'}),

            'fecha_baja': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

        }

    def clean_cantidad_animales(self):
        cantidad_animales = self.cleaned_data.get('cantidad_animales')
        if cantidad_animales < 1 or cantidad_animales > 30:
            raise forms.ValidationError("La cantidad de animales debe estar entre 1 y 30.")
        return cantidad_animales

    def clean_peso_ingreso(self):
        peso_ingreso = self.cleaned_data.get('peso_ingreso')
        cantidad_animales = self.cleaned_data.get('cantidad_animales')
        especie = self.cleaned_data.get('especie')
        peso_maximo_rata = 322
        peso_maximo_raton = 40
        peso_minimo_rata = 167
        peso_minimo_raton = 18

        if cantidad_animales and especie:
            peso_maximo = peso_maximo_rata if especie=='rata' else peso_maximo_raton
            peso_minimo = peso_minimo_rata if especie=='rata' else peso_minimo_raton
            peso_maximo_total = peso_maximo * cantidad_animales
            peso_minimo_total = peso_minimo * cantidad_animales

            if peso_ingreso < peso_minimo_total or peso_ingreso > peso_maximo_total:
                mensaje_validacion = f"El peso del lote debe estar entre {peso_minimo_total} y {peso_maximo_total} gramos, según la especie y la cantidad de animales ingresados"
                raise forms.ValidationError(mensaje_validacion)

        else:
            if not especie: raise forms.ValidationError("Primero ingrese la especie")
            if not cantidad_animales: raise forms.ValidationError("Primero ingrese la cantidad de animales")
            
        return peso_ingreso
        
