from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
from .models import UserEmail
import re
import logging

logger = logging.getLogger('core')


def home(request):
    try:
        logger.info('Home view called')
        return render(request, 'core/home.html')
    except Exception as e:
        logger.error(f'Error in home view: {str(e)}', exc_info=True)
        raise


def about(request):
    """About page view with language-aware slug handling"""
    from django.utils import translation
    from django.shortcuts import redirect
    
    lang = translation.get_language()
    # Get the path without language prefix (i18n_patterns removes it)
    current_path = request.path
    
    # If on English and accessing Serbian slug (o-nama), redirect to English slug
    if lang == 'en' and request.resolver_match.url_name == 'about':
        return redirect('core:about_en')
    # If on Serbian (Latin/Cyrillic) and accessing English slug (about_en), redirect to Serbian slug
    elif lang in ('sr-latn', 'sr-cyrl') and request.resolver_match.url_name == 'about_en':
        return redirect('core:about')
    
    return render(request, 'core/about.html')


@csrf_protect
@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact page view with language-aware slug handling"""
    from django.utils import translation
    from django.shortcuts import redirect
    
    lang = translation.get_language()
    
    # If on English and accessing Serbian slug (kontakt), redirect to English slug
    if lang == 'en' and request.resolver_match.url_name == 'contact':
        return redirect('core:contact_en')
    # If on Serbian (Latin/Cyrillic) and accessing English slug (contact_en), redirect to Serbian slug
    elif lang in ('sr-latn', 'sr-cyrl') and request.resolver_match.url_name == 'contact_en':
        return redirect('core:contact')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Basic validation
        errors = []
        if not name:
            errors.append(_('Ime je obavezno.'))
        if not surname:
            errors.append(_('Prezime je obavezno.'))
        if not phone:
            errors.append(_('Telefon je obavezan.'))
        if not email:
            errors.append(_('Email je obavezan.'))
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append(_('Email nije validan.'))
        if not message:
            errors.append(_('Poruka je obavezna.'))

        # Simple spam protection - check message length
        if len(message) < 10:
            errors.append(_('Poruka je prekratka.'))

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Save email to database (if not exists)
            UserEmail.objects.get_or_create(
                email=email,
                defaults={'source': 'contact'}
            )

            # Send email via SendGrid
            try:
                email_body = f"""
Nova poruka sa kontakt forme:

Ime: {name}
Prezime: {surname}
Telefon: {phone}
Email: {email}

Poruka:
{message}
"""
                # Use EmailMessage to set Reply-To header
                # This allows admin to click Reply and have the user's email in the "To" field
                email = EmailMessage(
                    subject=f'Nova poruka sa kontakt forme - {name} {surname}',
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_EMAIL],
                    reply_to=[email],  # Set Reply-To to user's email
                )
                email.send(fail_silently=False)
                messages.success(request, _('Poruka je uspešno poslata. Kontaktiraćemo vas uskoro.'))
                return redirect('core:contact')
            except Exception as e:
                messages.error(request, _('Došlo je do greške pri slanju poruke. Molimo pokušajte ponovo.'))

    return render(request, 'core/contact.html')
