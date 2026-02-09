from django import forms

class RestoreDatabaseForm(forms.Form):
    archivo_sql = forms.FileField(
        label="Archivo de respaldo (.sql)",
        help_text="Seleccione un archivo SQL válido"
    )
