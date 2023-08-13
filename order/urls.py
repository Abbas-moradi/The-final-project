from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='shopping-cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/del/<int:product_id>/', views.CartDelView.as_view(), name='cart_del'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('paid/', views.Paid.as_view(), name='paid'),
]