from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('cart/', views.Cart.as_view(), name='shopping-cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
]