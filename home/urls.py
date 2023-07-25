from django.urls import path
from . import views
from product.views import ProductDetail

app_name = 'home'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('shop/', views.Shop.as_view(), name='shop'),
    path('about/', views.About.as_view(), name='about'),
    path('details/', ProductDetail.as_view(), name='details'),
]