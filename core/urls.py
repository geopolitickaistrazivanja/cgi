from django.urls import path
from django.utils.translation import get_language
from . import views

app_name = 'core'

# Language-specific URL patterns
# Serbian (Latin and Cyrillic) use Serbian slugs, English uses English slugs
urlpatterns = [
    path('', views.home, name='home'),
    # Serbian slugs (for sr-latn and sr-cyrl)
    path('o-nama/', views.about, name='about'),
    path('kontakt/', views.contact, name='contact'),
    # English slugs
    path('about/', views.about, name='about_en'),
    path('contact/', views.contact, name='contact_en'),
]


