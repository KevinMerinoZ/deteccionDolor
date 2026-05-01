from django.urls import path
from usuario import views

app_name = 'usuario'

urlpatterns = [
    path('index/', views.pgUsuariosIndex, name='indexUsuario'),
    path('crear/', views.pgUsuariosCrear, name='crearUsuario'),
    path('editar/<int:id>', views.pgUsuariosEditar, name="editarUsuario"),
    path('eliminar/<int:id>', views.pgUsuariosEliminar, name="eliminarUsuario"),
    path('reporte-sesiones-exp/', views.reporteSesionesExp, name='reporteSesionesExp'),

    path('obtener_notificaciones/', views.obtener_notificaciones, name='obtenerNotificaciones'),
    path('actualizar-estado-notificacion/<int:id>/', views.actualizar_estado_notificacion, name='actualizar_estado_notificacion'),
    path('eliminar-notificacion/<int:id>/', views.eliminar_notificacion, name='eliminar_notificacion'),
    path('buscar-usuarios/', views.buscar_usuarios, name='buscar_usuarios'),
]