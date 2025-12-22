from django.urls import path
from . import views

app_name = 'protocoloExperimental'

urlpatterns = [
    path('', views.pgProtocoloIndex, name='indexProtocolo'),
    path('crear/', views.pgProtocoloCrear, name='crearProtocolo'),
    path('editar/<int:idProtocolo>/', views.pgProtocoloEditar, name='editarProtocolo'),
    path('eliminar/<int:idProtocolo>/', views.pgProtocoloEliminar, name='eliminarProtocolo'),

    # AJAX búsqueda dinámica
    path('buscar-protocolo/', views.buscarProtocolo, name='buscarProtocolo'),
]
