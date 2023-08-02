from django.urls import path
from .views import ProductCreateView, Products

app_name = 'product'

urlpatterns = [
    path('product/', ProductCreateView.as_view(), name='product-list-create'),
    path('', Products.as_view(), name='shop'),
    path('category/<slug:category_slug>/', Products.as_view(), name='category_filter')
]
