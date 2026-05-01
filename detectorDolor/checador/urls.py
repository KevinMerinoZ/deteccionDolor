from django.urls import path
from .views import checador_panel, asistencia_admin
app_name = 'checador'
urlpatterns = [
    path('panel/', checador_panel, name='checador_panel'),
    path('asistencia/', asistencia_admin, name='asistencia_admin'),
]
