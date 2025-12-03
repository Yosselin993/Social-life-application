from django.apps import AppConfig

class SFappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mysite'

    def ready(self):
        import mysite.signals