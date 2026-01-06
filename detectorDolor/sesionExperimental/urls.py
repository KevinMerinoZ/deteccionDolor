from django.urls import path
from . import views

app_name = 'sesionExperimental'

urlpatterns = [
    path('', views.pgSesionIndex, name='indexSesion'),
    path('crear/', views.pgSesionCrear, name='crearSesion'),
    path('editar/<int:idSesion>/', views.pgSesionEditar, name='editarSesion'),
    path('eliminar/<int:idSesion>/', views.pgSesionEliminar, name='eliminarSesion'),

    # AJAX
    path('buscar-sesion/', views.buscarSesion, name='buscarSesion'),
]
