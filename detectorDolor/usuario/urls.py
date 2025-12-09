from django.urls import path
from usuario import views

app_name = 'usuario'

urlpatterns = [
    path('index/', views.pgUsuariosIndex, name='indexUsuario'),
    path('crear/', views.pgUsuariosCrear, name='crearUsuario'),
    path('editar/<int:id>', views.pgUsuariosEditar, name="editarUsuario"),
    path('eliminar/<int:id>', views.pgUsuariosEliminar, name="eliminarUsuario"),
    path('buscar-usuarios/', views.buscar_usuarios, name='buscar_usuarios'),
]