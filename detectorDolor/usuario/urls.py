from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('principal/', views.pgPrincipal, name='principal'),
    path('index/', views.pgUsuariosIndex, name='index'),
    path('crear/', views.pgUsuariosCrear, name='crear'),
    path('editar/', views.pgUsuariosEditar, name="editar")
]