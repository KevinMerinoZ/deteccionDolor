from django.urls import path
from . import views

app_name = 'lotesAnimales'

urlpatterns = [
    path('', views.pgLotesIndex, name='indexLotes'),
    path('crear/', views.pgLotesCrear, name='crearLote'),
    path('editar/<int:id>', views.pgLotesEditar, name="editarLote"),
    path('eliminar/<int:id>', views.pgLotesEliminar, name="eliminarLote"),
    path('buscar-lotes/', views.buscar_lotes, name='buscar_lotes'),
]
