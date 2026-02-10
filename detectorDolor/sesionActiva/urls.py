from django.urls import path
from . import views

app_name = "sesionActiva"

urlpatterns = [
    # path("activarSesion/", views.activarSesion, name="activarS")
    path("tiempoSesion/", views.tiempoSesion, name="tiempoS")
]