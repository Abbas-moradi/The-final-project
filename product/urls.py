from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('api_product/', ProductCreateView.as_view(), name='product-list-create'),
    path('', Products.as_view(), name='shop'),
    path('category/<slug:category_slug>/', Products.as_view(), name='category_filter'),
    path('search_product', SearchProduct.as_view(), name='search_product'),
    path('comments/<int:pk>/', CommentView.as_view(), name='product_comment'),
    path('comments/', CommentView.as_view(), name='product_comment'),
    path('detail/<int:product_id>', ProductDetail.as_view(), name='product_detail'),
]
