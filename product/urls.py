from django.urls import path
from .views import ProductCreateView, Products

app_name = 'product'

urlpatterns = [
    path('product/', ProductCreateView.as_view(), name='product-list-create'),
    path('', Products.as_view(), name='shop')
]
