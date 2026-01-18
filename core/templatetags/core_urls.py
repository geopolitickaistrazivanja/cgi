"""
Template tags for language-aware URL generation
"""
from django import template
from django.urls import reverse, NoReverseMatch, resolve, Resolver404
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
            # Use correct namespace based on language
            namespace = 'topics-english' if lang == 'en' else 'topics-serbian'
            # Extract the URL name without namespace
            url_name = view_name.split(':', 1)[1]
            # Try to reverse with the correct namespace
            try:
                url_path = reverse(f'{namespace}:{url_name}', args=args)
            except NoReverseMatch:
                # Fallback to original namespace
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
            # Use correct namespace based on language
            namespace = 'accounts-english' if lang == 'en' else 'accounts-serbian'
            # Map to correct URL name based on language (similar to core URLs)
            url_name_map = {
                'accounts:register': 'register_en' if lang == 'en' else 'register',
                'accounts:login': 'login_en' if lang == 'en' else 'login',
                'accounts:logout': 'logout_en' if lang == 'en' else 'logout',
                'accounts:account': 'account_en' if lang == 'en' else 'account',
            }
            # Extract the URL name without namespace
            base_view_name = view_name.split(':', 1)[1]
            mapped_view_name = url_name_map.get(view_name, base_view_name)
            
            # Try to reverse with the correct namespace and mapped name
            try:
                url_path = reverse(f'{namespace}:{mapped_view_name}', args=args)
            except NoReverseMatch:
                # Fallback: try with original view name in correct namespace
                try:
                    url_path = reverse(f'{namespace}:{base_view_name}', args=args)
                except NoReverseMatch:
                    # Final fallback: try original view name with original namespace
                    url_path = reverse(view_name, args=args)
            
            # Replace base path and slugs based on language to ensure correctness
            # Use regex-like replacements: handle all variations systematically
            if lang == 'en':
                # For English, ensure /users/ base and English slugs
                # Replace ALL occurrences systematically - handle all language prefix variations
                replacements = [
                    # Language-prefixed base paths (must come first)
                    ('/en/korisnici/', '/en/users/'),
                    ('/sr-latn/korisnici/', '/sr-latn/korisnici/'),  # Shouldn't happen but safety
                    ('/sr-cyrl/korisnici/', '/sr-cyrl/korisnici/'),  # Shouldn't happen but safety
                    # Non-prefixed base paths
                    ('/korisnici/', '/users/'),
                    # Serbian slugs to English slugs
                    ('/registracija/', '/register/'),
                    ('/prijava/', '/login/'),
                    ('/odjava/', '/logout/'),
                    ('/nalog/', '/account/'),
                ]
            else:
                # For Serbian (Latin/Cyrillic), ensure /korisnici/ base and Serbian slugs
                # Replace ALL occurrences systematically
                replacements = [
                    # Language-prefixed base paths (must come first)
                    ('/en/users/', '/en/korisnici/'),
                    ('/sr-latn/users/', '/sr-latn/korisnici/'),
                    ('/sr-cyrl/users/', '/sr-cyrl/korisnici/'),
                    # Non-prefixed base paths
                    ('/users/', '/korisnici/'),
                    # English slugs to Serbian slugs
                    ('/register/', '/registracija/'),
                    ('/login/', '/prijava/'),
                    ('/logout/', '/odjava/'),
                    ('/account/', '/nalog/'),
                ]
            
            # Apply all replacements
            for old, new in replacements:
                if old in url_path:
                    url_path = url_path.replace(old, new, 1)  # Replace only first occurrence
            
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


@register.simple_tag(takes_context=True)
def convert_path_for_language(context, target_lang, current_path=None):
    """
    Convert the current URL path to the correct language-specific path.
    Used by language switcher to ensure URLs are correctly translated when switching languages.
    """
    if current_path is None:
        current_path = context['request'].path
    
    # Convert path based on target language
    converted_path = current_path
    
    # Handle accounts URLs
    if '/korisnici/' in current_path or '/users/' in current_path:
        if target_lang == 'en':
            # Convert to English
            converted_path = converted_path.replace('/korisnici/', '/users/', 1)
            converted_path = converted_path.replace('/en/korisnici/', '/en/users/', 1)
            converted_path = converted_path.replace('/sr-latn/korisnici/', '/sr-latn/korisnici/', 1)
            converted_path = converted_path.replace('/sr-cyrl/korisnici/', '/sr-cyrl/korisnici/', 1)
            converted_path = converted_path.replace('/registracija/', '/register/', 1)
            converted_path = converted_path.replace('/prijava/', '/login/', 1)
            converted_path = converted_path.replace('/odjava/', '/logout/', 1)
            converted_path = converted_path.replace('/nalog/', '/account/', 1)
        else:
            # Convert to Serbian
            converted_path = converted_path.replace('/users/', '/korisnici/', 1)
            converted_path = converted_path.replace('/en/users/', '/en/korisnici/', 1)
            converted_path = converted_path.replace('/sr-latn/users/', '/sr-latn/korisnici/', 1)
            converted_path = converted_path.replace('/sr-cyrl/users/', '/sr-cyrl/korisnici/', 1)
            converted_path = converted_path.replace('/register/', '/registracija/', 1)
            converted_path = converted_path.replace('/login/', '/prijava/', 1)
            converted_path = converted_path.replace('/logout/', '/odjava/', 1)
            converted_path = converted_path.replace('/account/', '/nalog/', 1)
    
    # Handle topics URLs
    if '/teme/' in current_path or '/topics/' in current_path:
        if target_lang == 'en':
            converted_path = converted_path.replace('/teme/', '/topics/', 1)
            converted_path = converted_path.replace('/en/teme/', '/en/topics/', 1)
        else:
            converted_path = converted_path.replace('/topics/', '/teme/', 1)
            converted_path = converted_path.replace('/en/topics/', '/en/teme/', 1)
            converted_path = converted_path.replace('/sr-latn/topics/', '/sr-latn/teme/', 1)
            converted_path = converted_path.replace('/sr-cyrl/topics/', '/sr-cyrl/teme/', 1)
    
    # Handle core URLs (about, contact)
    if '/o-nama/' in current_path or '/about/' in current_path:
        if target_lang == 'en':
            converted_path = converted_path.replace('/o-nama/', '/about/', 1)
            converted_path = converted_path.replace('/en/o-nama/', '/en/about/', 1)
        else:
            converted_path = converted_path.replace('/about/', '/o-nama/', 1)
            converted_path = converted_path.replace('/en/about/', '/en/o-nama/', 1)
    
    if '/kontakt/' in current_path or '/contact/' in current_path:
        if target_lang == 'en':
            converted_path = converted_path.replace('/kontakt/', '/contact/', 1)
            converted_path = converted_path.replace('/en/kontakt/', '/en/contact/', 1)
        else:
            converted_path = converted_path.replace('/contact/', '/kontakt/', 1)
            converted_path = converted_path.replace('/en/contact/', '/en/kontakt/', 1)
    
    return converted_path
