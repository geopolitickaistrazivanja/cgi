from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django import forms
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import gettext_lazy as _
from core.models import UserEmail


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=False, label=_('Email'))

    class Meta:
        model = BaseUserCreationForm.Meta.model
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('email'):
            user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


@csrf_protect
@require_http_methods(["GET", "POST"])
def register(request):
    """Register view with language-aware slug handling"""
    from django.utils import translation
    
    lang = translation.get_language()
    current_path = request.path
    
    # If on English and accessing Serbian slug, redirect to English slug
    if lang == 'en' and request.resolver_match.url_name == 'register':
        from django.urls import reverse
        register_url = reverse('accounts-english:register_en')
        return redirect(register_url)
    # If on Serbian (Latin/Cyrillic) and accessing English slug, redirect to Serbian slug
    elif lang in ('sr-latn', 'sr-cyrl') and request.resolver_match.url_name == 'register_en':
        from django.urls import reverse
        register_url = reverse('accounts-serbian:register')
        return redirect(register_url)
    
    if request.user.is_authenticated:
        # Redirect to correct account URL based on language using proper namespace
        from django.urls import reverse
        lang = translation.get_language()
        namespace = 'accounts-english' if lang == 'en' else 'accounts-serbian'
        url_name = 'account_en' if lang == 'en' else 'account'
        account_url = reverse(f'{namespace}:{url_name}')
        return redirect(account_url)
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email', '')
            if email:
                UserEmail.objects.get_or_create(
                    email=email,
                    defaults={'source': 'registration'}
                )
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, _('Uspešno ste se registrovali.'))
                # Redirect to correct account URL based on language using proper namespace
                from django.urls import reverse
                lang = translation.get_language()
                namespace = 'accounts-english' if lang == 'en' else 'accounts-serbian'
                url_name = 'account_en' if lang == 'en' else 'account'
                account_url = reverse(f'{namespace}:{url_name}')
                return redirect(account_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login view with language-aware slug handling"""
    from django.utils import translation
    
    lang = translation.get_language()
    current_path = request.path
    
    # If on English and accessing Serbian slug, redirect to English slug
    if lang == 'en' and request.resolver_match.url_name == 'login':
        from django.urls import reverse
        login_url = reverse('accounts-english:login_en')
        return redirect(login_url)
    # If on Serbian (Latin/Cyrillic) and accessing English slug, redirect to Serbian slug
    elif lang in ('sr-latn', 'sr-cyrl') and request.resolver_match.url_name == 'login_en':
        from django.urls import reverse
        login_url = reverse('accounts-serbian:login')
        return redirect(login_url)
    
    if request.user.is_authenticated:
        # Redirect to correct account URL based on language using proper namespace
        from django.urls import reverse
        namespace = 'accounts-english' if lang == 'en' else 'accounts-serbian'
        url_name = 'account_en' if lang == 'en' else 'account'
        account_url = reverse(f'{namespace}:{url_name}')
        return redirect(account_url)
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, _('Molimo unesite korisničko ime i lozinku.'))
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('Uspešno ste se prijavili.'))
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                # Redirect to correct account URL based on language using proper namespace
                from django.urls import reverse
                namespace = 'accounts-english' if lang == 'en' else 'accounts-serbian'
                url_name = 'account_en' if lang == 'en' else 'account'
                account_url = reverse(f'{namespace}:{url_name}')
                return redirect(account_url)
            else:
                messages.error(request, _('Pogrešno korisničko ime ili lozinka. Molimo pokušajte ponovo.'))
    
    return render(request, 'accounts/login.html')


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Logout view with language-aware slug handling"""
    from django.utils import translation
    
    lang = translation.get_language()
    
    # If on English and accessing Serbian slug, redirect to English slug
    if lang == 'en' and request.resolver_match.url_name == 'logout':
        from django.urls import reverse
        logout_url = reverse('accounts-english:logout_en')
        return redirect(logout_url)
    # If on Serbian (Latin/Cyrillic) and accessing English slug, redirect to Serbian slug
    elif lang in ('sr-latn', 'sr-cyrl') and request.resolver_match.url_name == 'logout_en':
        from django.urls import reverse
        logout_url = reverse('accounts-serbian:logout')
        return redirect(logout_url)
    
    if request.user.is_authenticated:
        logout(request)
        # Simple success message without link (link removed to avoid duplicate messages)
        messages.success(request, _('Uspešno ste se odjavili.'))
    
    # Redirect to the page user was on, or home page
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER', '/')
    # Avoid redirecting back to logout page (check both Serbian and English slugs)
    if '/odjava/' in next_url or '/korisnici/odjava/' in next_url or '/logout/' in next_url or '/users/logout/' in next_url:
        next_url = '/'
    return redirect(next_url)


@require_http_methods(["GET"])
def account(request):
    """Account view with language-aware slug handling"""
    from django.utils import translation
    
    lang = translation.get_language()
    
    # If on English and accessing Serbian slug, redirect to English slug
    if lang == 'en' and request.resolver_match.url_name == 'account':
        from django.urls import reverse
        account_url = reverse('accounts-english:account_en')
        return redirect(account_url)
    # If on Serbian (Latin/Cyrillic) and accessing English slug, redirect to Serbian slug
    elif lang in ('sr-latn', 'sr-cyrl') and request.resolver_match.url_name == 'account_en':
        from django.urls import reverse
        account_url = reverse('accounts-serbian:account')
        return redirect(account_url)
    
    if not request.user.is_authenticated:
        # Redirect to correct login URL based on language using proper namespace
        from django.urls import reverse
        namespace = 'accounts-english' if lang == 'en' else 'accounts-serbian'
        url_name = 'login_en' if lang == 'en' else 'login'
        login_url = reverse(f'{namespace}:{url_name}')
        return redirect(login_url)
    
    context = {}
    return render(request, 'accounts/account.html', context)
