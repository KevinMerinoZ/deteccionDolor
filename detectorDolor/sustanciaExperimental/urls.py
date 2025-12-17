from django.urls import path
from . import views

app_name = 'sustanciaExperimental'

urlpatterns = [
    path('', views.pgSustanciaIndex, name='indexSustancia'),
    path('crear/', views.pgSustanciaCrear, name='crearSustancia'),
    path('editar/<int:idsustanciaExperimental>/', views.pgSustanciaEditar, name='editarSustancia'),
    path('eliminar/<int:idsustanciaExperimental>/', views.pgSustanciaEliminar, name='eliminarSustancia'),

    # AJAX búsqueda dinámica
    path('buscar-sustancia/', views.buscarSustancia, name='buscarSustancia'),
]
