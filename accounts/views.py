from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django import forms
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import gettext_lazy as _
from core.models import UserEmail
from accounts.models import Order


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


@require_http_methods(["GET"])
def account(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/account.html', context)
