from django import forms
from .models import Cita
from usuario.models import Usuario

from django.utils import timezone
from datetime import datetime, date, time


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            'fecha',
            'horaInicio',
            'horaFin',
            'sala_laboratorio',
            'usuario',
            'protocolo_experimental',
        ]

        widgets = {
            'fecha': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'horaInicio': forms.TimeInput(format=('%H:%M'), attrs={'class': 'form-control', 'type': 'time'}),
            'horaFin': forms.TimeInput(format=('%H:%M'), attrs={'class': 'form-control', 'type': 'time'}),

            'sala_laboratorio': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'protocolo_experimental': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        fechaActual = timezone.localtime(timezone.now()).date()
        if fecha < fechaActual:
            raise forms.ValidationError("La fecha no puede ser anterior a la fecha actual.")
        return fecha

    def clean_horaInicio(self):
        horaInicio = self.cleaned_data.get('horaInicio')
        fechaActual = timezone.localtime(timezone.now())
        fecha = self.cleaned_data.get('fecha')

        if fecha:
            fecha_horiaInicio = timezone.make_aware(datetime.combine(fecha, horaInicio))
            if fecha_horiaInicio < fechaActual:
                raise forms.ValidationError("La hora de inicio no puede ser anterior a la hora actual.")

        else:
            raise forms.ValidationError("La fecha debe ser proporcionada antes de la hora de inicio")
        
        return horaInicio

    def clean_horaFin(self):
        horaFin = self.cleaned_data.get('horaFin')
        horaInicio = self.cleaned_data.get('horaInicio')
        fechaActual = timezone.localtime(timezone.now())
        fecha = self.cleaned_data.get('fecha')

        if fecha:
            if horaInicio is None:
                raise forms.ValidationError("La hora de inicio debe ser proporcionada antes de la hora de fin.")
            
            else:
                fecha_horiaInicio = timezone.make_aware(datetime.combine(fecha, horaInicio))
                fecha_horaFin = timezone.make_aware(datetime.combine(fecha, horaFin))
                print("fecha horaInicio: ", fecha_horiaInicio)
                print("fecha horaFin: ", fecha_horaFin)
                if fecha_horaFin < fechaActual:
                    raise forms.ValidationError("La hora de fin no puede ser anterior a la hora actual.")
                
                if fecha_horaFin <= fecha_horiaInicio:
                    raise forms.ValidationError("Lahora de fin debe ser posterior a la hora de inicio.")
                 
                elif diffHora(horaInicio, horaFin) < 30:
                    raise forms.ValidationError("La duración mínima de la cita es de 30 minutos.")
                
                elif diffHora(horaInicio, horaFin) > 360:
                    raise forms.ValidationError("La duración máxima de la cita es de 6 horas.")
        else:
            raise forms.ValidationError("La fecha debe ser proporcionada antes de la hora de fin")
        return horaFin

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sala_laboratorio'].queryset = self.fields['sala_laboratorio'].queryset.filter(is_active=True).order_by('nombre')
        self.fields['protocolo_experimental'].queryset = self.fields['protocolo_experimental'].queryset.filter(is_active=True).order_by('nombre_protocolo')

        self.fields['usuario'].queryset = Usuario.objects.filter(is_active=True).order_by('user__username')
        self.fields["usuario"].label_from_instance = lambda obj: obj.user.username

        self.fields['fecha'].required = True
        self.fields['fecha'].initial = None
        self.fields['horaInicio'].required = True
        self.fields['horaInicio'].initial = None
        self.fields['horaFin'].required = True
        self.fields['horaFin'].initial = None

        # Esto asegura que el valor se formatee correctamente al cargar el formulario
        if not user.groups.filter(name='administrador').exists():
            self.fields.pop('usuario')
            
        if self.instance and self.instance.pk:
            if self.instance.fecha:
                self.initial['fecha'] = self.instance.fecha
            if self.instance.horaInicio:
                self.initial['horaInicio'] = self.instance.horaInicio
            if self.instance.horaFin:
                self.initial['horaFin'] = self.instance.horaFin

def diffHora(hora_inicio:time, hora_fin:time):
    print("date.min", date.min)
    fechaInicio = datetime.combine(date.min, hora_inicio)
    fechaFin = datetime.combine(date.min, hora_fin)
    return (fechaFin - fechaInicio).total_seconds()/60