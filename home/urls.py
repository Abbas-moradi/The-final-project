from django.urls import path
from . import views
from product.views import *

app_name = 'home'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('about/', views.About.as_view(), name='about'),
    path('details/', ProductDetail.as_view(), name='details'),
    path('profile/', UserProfile.as_view(), name='profile'),
]