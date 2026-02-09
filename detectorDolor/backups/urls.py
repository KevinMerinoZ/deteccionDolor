from django.urls import path
from . import views
app_name = 'backups'
urlpatterns = [
    path('', views.backup_panel, name='backup_panel'),
    path('backups/', views.backup_database, name='backup_db'),
    path('restore/', views.restore_database, name='restore_db'),
]
