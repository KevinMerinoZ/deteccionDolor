from django.urls import path
from . import views

app_name = 'provedor'

urlpatterns = [
    path('', views.pgProveedorIndex, name='indexProveedor'),
    path('crear/', views.pgProveedorCrear, name='crearProveedor'),
    path('editar/<int:idProveedor>/', views.pgProveedorEditar, name='editarProveedor'),
    path('eliminar/<int:idProveedor>/', views.pgProveedorEliminar, name='eliminarProveedor'),

    # AJAX búsqueda dinámica
    path('buscar-proveedor/', views.buscarProveedor, name='buscarProveedor'),
]
