from django.urls import path
from . import views

app_name = 'material'

urlpatterns = [
    path('', views.pgMaterialIndex, name='indexMaterial'),
    path('crear/', views.pgMaterialCrear, name='crearMaterial'),
    path('editar/<int:idmateriales>/', views.pgMaterialEditar, name='editarMaterial'),
    path('eliminar/<int:idmateriales>/', views.pgMaterialEliminar, name='eliminarMaterial'),

    # AJAX búsqueda dinámica
    path('buscar-material/', views.buscarMaterial, name='buscarMaterial'),
]
