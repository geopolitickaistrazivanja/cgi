from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('proizvod/<slug:slug>/', views.product_detail, name='product_detail'),
    path('dodaj-u-korpu/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('ukloni-iz-korpe/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('azuriraj-korpu/<int:product_id>/', views.update_cart, name='update_cart'),
    path('korpa/', views.cart_view, name='cart'),
    path('korpa-dropdown/', views.cart_dropdown, name='cart_dropdown'),
    path('placanje/', views.checkout, name='checkout'),
    path('pretraga/', views.search_products, name='search_products'),
]

