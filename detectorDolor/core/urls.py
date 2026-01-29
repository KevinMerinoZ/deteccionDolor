from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('interfazPrincipal/', views.interfazPrincipal, name='interfazPrincipal'),
]