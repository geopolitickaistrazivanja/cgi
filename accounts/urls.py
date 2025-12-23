from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('registracija/', views.register, name='register'),
    path('prijava/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('odjava/', auth_views.LogoutView.as_view(), name='logout'),
    path('nalog/', views.account, name='account'),
]

