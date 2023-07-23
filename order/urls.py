from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('cart/', views.Cart.as_view(), name='shopping-cart'),
    path('cart/', views.Checkout.as_view(), name='checkout'),
]