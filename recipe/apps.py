from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'recipe'

    def ready(self):
        import recipe.signals
