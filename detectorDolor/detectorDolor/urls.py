"""
URL configuration for detectorDolor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth import views as auth_views
# from inicioSesion import views
from usuario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inicioSesion.urls', namespace='inicioSesion')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('usuarios/', include('usuario.urls', namespace='usuario')), #activar despues
    path('lotesAnimales/', include('lotesAnimales.urls', namespace='lotesAnimales')),
    path('provedor/', include('provedor.urls', namespace='provedor')),
    path('farmaco/', include('farmaco.urls', namespace='farmaco')),
    path('material/', include('material.urls', namespace='material')),
    path('sustanciasExperimentales/', include('sustanciaExperimental.urls', namespace='sustanciaExperimental')),
    path('protocolosExperimentales/', include('protocoloExperimental.urls', namespace='protocoloExperimental')),
    path('citas/', include('cita.urls', namespace='cita')),
    path('sesionesExperimentales/', include('sesionExperimental.urls', namespace='sesionExperimental')),
    path('detectorDolorApp/', include('detectorDolor_app.urls', namespace='detectorDolorApp')),
    path('core/', include('core.urls', namespace='core')),
]
