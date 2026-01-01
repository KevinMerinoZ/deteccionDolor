from django.urls import path
from . import views

app_name = 'cita'

urlpatterns = [
    path('', views.pgCitaIndex, name='indexCita'),
    path('crear/', views.pgCitaCrear, name='crearCita'),
    path('editar/<int:idcitas>/', views.pgCitaEditar, name='editarCita'),
    path('eliminar/<int:idcitas>/', views.pgCitaEliminar, name='eliminarCita'),

    # AJAX búsqueda dinámica
    path('buscar-cita/', views.buscarCita, name='buscarCita'),
]
