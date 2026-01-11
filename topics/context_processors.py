from .models import Category


def categories(request):
    """Add categories to template context for navigation menus"""
    return {
        'categories': Category.objects.all().order_by('name')
    }
