from django import template

register = template.Library()

@register.filter
def format_price(value):
    """Format price with thousands separator, no decimals"""
    if value is None:
        return "Izaberite opcije"
    try:
        return f"{int(float(value)):,} RSD"
    except (ValueError, TypeError):
        return "Izaberite opcije"


