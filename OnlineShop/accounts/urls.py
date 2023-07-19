from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRfgisterView.as_view(), name='user_register'),
]