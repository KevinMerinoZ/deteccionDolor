from django.urls import path
from . import views

app_name = 'bitacoraMaterialesEliminados'

urlpatterns = [
    path('index/', views.pgbitacoraMaterialesIndex, name='index_materiales_eliminados'),
    path('crear/', views.pgbitacoraMaterialesCrear, name='crear_materiales_eliminados'),
    path('editar/<int:id>', views.pgbitacoraMaterialesEditar, name="editar_materiales_eliminados"),
    path('eliminar/<int:id>', views.pgbitacoraMaterialesEliminar, name="eliminar_materiales_eliminados"),

    path('buscar-materiales/', views.buscarMaterialesEliminados, name='buscar_materiales_eliminados'),
]
