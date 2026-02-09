from django import forms
from .models import IncidenciaExperimental
from sesionExperimental.models import SesionExperimental

class IncidenciaExperimentalforms(forms.ModelForm):
    class Meta:
        model = IncidenciaExperimental 
        fields = ['fecha',
            'descripcion',
            'idSesionExperimental']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'idSesionExperimental': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # recibimos el usuario
        super().__init__(*args, **kwargs)

        if user:
            self.fields['idSesionExperimental'].queryset = \
                SesionExperimental.objects.filter(usuario__user__username=user)
        
        
        
       