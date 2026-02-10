from django.urls import path
from .views import checador_panel
app_name = 'checador'
urlpatterns = [
    path('panel/', checador_panel, name='checador_panel'),
]
