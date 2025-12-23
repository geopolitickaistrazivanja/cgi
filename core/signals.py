"""
Signal handlers for core app.
"""
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .upload_tracker import cleanup_old_tracking_records


@receiver(post_migrate)
def cleanup_old_tracking_on_migrate(sender, **kwargs):
    """
    Clean up old tracking records after migrations.
    This helps keep the database clean.
    """
    if sender.name == 'core':
        try:
            cleanup_old_tracking_records()
        except Exception:
            pass  # Ignore errors

