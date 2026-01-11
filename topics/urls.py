from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/', views.topic_detail, name='topic_detail'),
]


