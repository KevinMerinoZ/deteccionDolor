from django.urls import path
from . import views

app_name = 'farmaco'

urlpatterns = [
    path('', views.pgFarmacoIndex, name='indexFarmaco'),
    path('crear/', views.pgFarmacoCrear, name='crearFarmaco'),
    path('editar/<int:idfarmacos>/', views.pgFarmacoEditar, name='editarFarmaco'),
    path('eliminar/<int:idfarmacos>/', views.pgFarmacoEliminar, name='eliminarFarmaco'),

    # AJAX búsqueda dinámica
    path('buscar-farmaco/', views.buscarFarmaco, name='buscarFarmaco'),
]
