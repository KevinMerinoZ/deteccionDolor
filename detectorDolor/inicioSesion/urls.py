from django.urls import path
from . import views

app_name = 'inicioSesion'

urlpatterns = [
    path('', views.login_vista, name='login'),
    path('recuperacionContrasena/', views.recuperarContrasena, name='recuperacionContrasena'),
]
