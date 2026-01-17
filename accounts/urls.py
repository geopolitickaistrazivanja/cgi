from django.urls import path
from . import views

app_name = 'accounts'

# Language-specific URL patterns
# Serbian (Latin and Cyrillic) use Serbian slugs, English uses English slugs
urlpatterns = [
    # Serbian slugs (for sr-latn and sr-cyrl)
    path('registracija/', views.register, name='register'),
    path('prijava/', views.login_view, name='login'),
    path('odjava/', views.logout_view, name='logout'),
    path('nalog/', views.account, name='account'),
    # English slugs
    path('register/', views.register, name='register_en'),
    path('login/', views.login_view, name='login_en'),
    path('logout/', views.logout_view, name='logout_en'),
    path('account/', views.account, name='account_en'),
]


