from django.urls import path
from usuario import views

app_name = 'usuario'

urlpatterns = [
    path('principal/', views.pgPrincipal, name='principal'),
    path('index/', views.pgUsuariosIndex, name='index'),
    path('crear/', views.pgUsuariosCrear, name='crear'),
    path('editar/<int:id>', views.pgUsuariosEditar, name="editar"),
    path('eliminar/<int:id>', views.pgUsuariosEliminar, name="eliminarUsuario"),
    path('buscar-usuarios/', views.buscar_usuarios, name='buscar_usuarios'),
]