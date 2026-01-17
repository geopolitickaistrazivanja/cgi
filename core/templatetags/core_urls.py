"""
Template tags for language-aware URL generation
"""
from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag(takes_context=True)
def lang_url(context, view_name, *args):
    """
    Generate URL based on current language.
    For Serbian (Latin/Cyrillic): use Serbian URL names (about, contact)
    For English: use English URL names (about_en, contact_en)
    For topics URLs: use 'teme' base for Serbian, 'topics' base for English
    """
    from django.urls import resolve
    lang = get_language()
    
    # Handle topics URLs specially - need to manually construct with correct base path
    if view_name.startswith('topics:'):
        try:
            # Reverse the URL - Django will return path with one of the base paths
            url_path = reverse(view_name, args=args)
            
            # Replace base path based on language
            if lang == 'en':
                # For English, ensure /topics/ base (replace /teme/ if present)
                url_path = url_path.replace('/teme/', '/topics/', 1)
                url_path = url_path.replace('/en/teme/', '/en/topics/', 1)
            else:
                # For Serbian (Latin/Cyrillic), ensure /teme/ base (replace /topics/ if present)
                url_path = url_path.replace('/topics/', '/teme/', 1)
                url_path = url_path.replace('/en/topics/', '/en/teme/', 1)
                url_path = url_path.replace('/sr-latn/topics/', '/sr-latn/teme/', 1)
                url_path = url_path.replace('/sr-cyrl/topics/', '/sr-cyrl/teme/', 1)
            
            return url_path
        except NoReverseMatch:
            return '#'
    
    # Handle accounts URLs specially - need to manually construct with correct base path
    if view_name.startswith('accounts:'):
        try:
            # Map to correct URL name based on language (similar to core URLs)
            url_name_map = {
                'accounts:register': 'accounts:register_en' if lang == 'en' else 'accounts:register',
                'accounts:login': 'accounts:login_en' if lang == 'en' else 'accounts:login',
                'accounts:logout': 'accounts:logout_en' if lang == 'en' else 'accounts:logout',
                'accounts:account': 'accounts:account_en' if lang == 'en' else 'accounts:account',
            }
            mapped_view_name = url_name_map.get(view_name, view_name)
            
            # Try to reverse with the mapped name first
            try:
                url_path = reverse(mapped_view_name, args=args)
            except NoReverseMatch:
                # Fallback to original view name
                url_path = reverse(view_name, args=args)
            
            # Replace base path and slugs based on language to ensure correctness
            # Important: Replace language-prefixed paths FIRST, then non-prefixed
            if lang == 'en':
                # For English, ensure /users/ base and English slugs
                # Replace language-prefixed base paths first
                url_path = url_path.replace('/en/korisnici/', '/en/users/', 1)
                url_path = url_path.replace('/sr-latn/users/', '/sr-latn/korisnici/', 1)
                url_path = url_path.replace('/sr-cyrl/users/', '/sr-cyrl/korisnici/', 1)
                # Then replace non-prefixed base paths
                url_path = url_path.replace('/korisnici/', '/users/', 1)
                # Replace Serbian slugs with English slugs
                url_path = url_path.replace('/registracija/', '/register/', 1)
                url_path = url_path.replace('/prijava/', '/login/', 1)
                url_path = url_path.replace('/odjava/', '/logout/', 1)
                url_path = url_path.replace('/nalog/', '/account/', 1)
            else:
                # For Serbian (Latin/Cyrillic), ensure /korisnici/ base and Serbian slugs
                # Replace language-prefixed base paths first
                url_path = url_path.replace('/en/users/', '/en/korisnici/', 1)
                url_path = url_path.replace('/sr-latn/users/', '/sr-latn/korisnici/', 1)
                url_path = url_path.replace('/sr-cyrl/users/', '/sr-cyrl/korisnici/', 1)
                # Then replace non-prefixed base paths
                url_path = url_path.replace('/users/', '/korisnici/', 1)
                # Replace English slugs with Serbian slugs
                url_path = url_path.replace('/register/', '/registracija/', 1)
                url_path = url_path.replace('/login/', '/prijava/', 1)
                url_path = url_path.replace('/logout/', '/odjava/', 1)
                url_path = url_path.replace('/account/', '/nalog/', 1)
            
            return url_path
        except NoReverseMatch:
            return '#'
    
    # Map URL names based on language for core URLs
    url_map = {
        'core:about': 'core:about_en' if lang == 'en' else 'core:about',
        'core:contact': 'core:contact_en' if lang == 'en' else 'core:contact',
    }
    
    # Use mapped URL name if available, otherwise use the original
    mapped_name = url_map.get(view_name, view_name)
    
    try:
        return reverse(mapped_name, args=args)
    except NoReverseMatch:
        # Fallback to original if mapped fails
        try:
            return reverse(view_name, args=args)
        except NoReverseMatch:
            return '#'
