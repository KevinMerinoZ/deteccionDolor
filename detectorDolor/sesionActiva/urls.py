from django.urls import path
from . import views

app_name = "sesionActiva"

urlpatterns = [
    # path("activarSesion/", views.activarSesion, name="activarS")
    path("", views.indexSesion, name="indexSesionActiva"),
    path("tiempoSesion/", views.tiempoSesion, name="tiempoSesionActiva"),
    path("cerrarSesion/<int:idUsuario>/", views.cerrarSesion, name="cerrarSesionActiva"),
    path("reporteActividadUsuario/", views.reporte_actividad_usuario, name="reporteActividadUsuario"),

    path("buscar-sesionesActivas/", views.buscarActividadUsuario, name="buscarSesionesActivas"),
]