from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'backend.api'
    # name = 'api'

    def ready(self):
        import backend.api.signals
