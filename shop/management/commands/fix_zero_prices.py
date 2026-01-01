from django.core.management.base import BaseCommand
from shop.models import ProductDimension


class Command(BaseCommand):
    help = 'Lists or fixes ProductDimension records with price=0'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Delete dimensions with price=0 (use with caution)',
        )

    def handle(self, *args, **options):
        zero_price_dims = ProductDimension.objects.filter(price=0)
        count = zero_price_dims.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No dimensions with price=0 found. All good!')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'Found {count} dimension(s) with price=0:')
        )
        
        for dim in zero_price_dims:
            self.stdout.write(
                f'  - {dim.product.title}: {dim.get_display()} (ID: {dim.id})'
            )
        
        if options['fix']:
            zero_price_dims.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Deleted {count} dimension(s) with price=0')
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    '\nTo delete these dimensions, run: python manage.py fix_zero_prices --fix\n'
                    'Or update their prices manually in the admin.'
                )
            )


