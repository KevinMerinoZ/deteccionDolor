from django.urls import path
from notificacion import views

app_name = "Notificacion"

urlpatterns =[
    path('obtener_notificaciones/', views.obtener_notificaciones, name='obtenerNotificaciones'),
    path('actualizar-estado-notificacion/<int:id>/', views.actualizar_estado_notificacion, name='actualizar_estado_notificacion'),
    path('eliminar-notificacion/<int:id>/', views.eliminar_notificacion, name='eliminar_notificacion'),
]