from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        # Import signal handlers
        import core.signals  # noqa
        
        # Schedule periodic cleanup of old tracking records
        # This runs after migrations
        from .upload_tracker import cleanup_old_tracking_records
        try:
            cleanup_old_tracking_records()
        except Exception:
            pass  # Ignore errors during startup
