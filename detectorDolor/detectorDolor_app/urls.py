from django.urls import path
from . import views

app_name = 'detectorDolorApp'

urlpatterns=[
    path('<int:idSesion>', views.index, name='indexDetector'),
]