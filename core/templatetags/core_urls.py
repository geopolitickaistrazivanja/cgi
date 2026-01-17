"""
Template tags for language-aware URL generation
"""
from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag(takes_context=True)
def lang_url(context, view_name):
    """
    Generate URL based on current language.
    For Serbian (Latin/Cyrillic): use Serbian URL names (about, contact)
    For English: use English URL names (about_en, contact_en)
    """
    lang = get_language()
    
    # Map URL names based on language
    url_map = {
        'core:about': 'core:about_en' if lang == 'en' else 'core:about',
        'core:contact': 'core:contact_en' if lang == 'en' else 'core:contact',
    }
    
    # Use mapped URL name if available, otherwise use the original
    mapped_name = url_map.get(view_name, view_name)
    
    try:
        return reverse(mapped_name)
    except NoReverseMatch:
        # Fallback to original if mapped fails
        try:
            return reverse(view_name)
        except NoReverseMatch:
            return '#'
