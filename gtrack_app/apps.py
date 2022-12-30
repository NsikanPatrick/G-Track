from django.apps import AppConfig


class GtrackAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gtrack_app'

    def ready(self):
        from gtrack_app import signals