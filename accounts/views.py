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
    if request.user.is_authenticated:
        return redirect('accounts:account')
    
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
                return redirect('accounts:account')
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
    if request.user.is_authenticated:
        return redirect('accounts:account')
    
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
                return redirect('accounts:account')
            else:
                messages.error(request, _('Pogrešno korisničko ime ili lozinka. Molimo pokušajte ponovo.'))
    
    return render(request, 'accounts/login.html')


@require_http_methods(["GET", "POST"])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        # Create a success message with a link to login
        from django.utils.safestring import mark_safe
        from django.urls import reverse
        login_url = reverse('accounts:login')
        message = mark_safe(_('Uspešno ste se odjavili. <a href="{}">Prijavite se ponovo</a>').format(login_url))
        messages.success(request, message)
    
    # Redirect to the page user was on, or home page
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER', '/')
    # Avoid redirecting back to logout page
    if '/odjava/' in next_url or '/korisnici/odjava/' in next_url:
        next_url = '/'
    return redirect(next_url)


@require_http_methods(["GET"])
def account(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    context = {}
    return render(request, 'accounts/account.html', context)
