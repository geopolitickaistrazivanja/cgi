"""
Management command to clean up old CKEditor upload tracking records.
Run this periodically (e.g., daily via cron) to keep the database clean.

Usage:
    python manage.py cleanup_tracking
"""
from django.core.management.base import BaseCommand
from core.upload_tracker import cleanup_old_tracking_records


class Command(BaseCommand):
    help = 'Clean up old CKEditor upload tracking records'

    def handle(self, *args, **options):
        self.stdout.write('Cleaning up old tracking records...')
        
        try:
            cleanup_old_tracking_records()
            self.stdout.write(
                self.style.SUCCESS('Successfully cleaned up old tracking records')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error cleaning up tracking records: {e}')
            )

