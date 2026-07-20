from django.urls import path
from . import views

app_name = 'detectorDolorApp'

urlpatterns=[
    path('<int:idSesion>', views.index, name='indexDetector'),
    path('<int:idSesion>/<str:accion>', views.index, name='indexDetector'),
    path('reporteResultados/<int:idSesion>', views.reporte_resultados_dolor, name='reporteResultados'),
    
    path('CuestionarioPrincipal', views.cuestionario_principal, name='cuestionarioPrincipal'),
]