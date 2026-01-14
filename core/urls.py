from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('o-nama/', views.about, name='about'),
    path('kontakt/', views.contact, name='contact'),
]


