from django.apps import AppConfig


class SesionactivaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sesionActiva'

    def ready(self):
        import sesionActiva.signals
        return super().ready()