from django.urls import path
from . import views
app_name = 'gestionIncidencias'
urlpatterns = [
    path('', views.IncidenciasIndex, name='indexIncidencias'),
    path('crear/', views.IncidenciasCrear, name='crearIncidencias'),
    path('editar/<int:idIncidencia>/', views.IncidenciasEditar, name='editarIncidencias'),
    path('eliminar/<int:idIncidencia>/', views.IncidenciasEliminar, name='eliminarIncidencias'),

    # AJAX búsqueda dinámica
    path('buscar-Incidencia/', views.buscarIncidencia, name='buscarIncidencia'),
]