from django.apps import AppConfig


class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community'

    def ready(self, *args, **kwargs):
        import community.signals
        return super().ready(*args, **kwargs)
