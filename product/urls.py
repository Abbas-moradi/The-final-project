from django.urls import path
from .views import ProductCreateView

app_name = 'product'

urlpatterns = [
    path('product/', ProductCreateView.as_view(), name='product-list-create'),
]
