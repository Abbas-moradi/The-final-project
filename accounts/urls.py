from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UsreLoginView.as_view(), name='user_login'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('user/', views.UserCreateView.as_view(), name='user-list-create'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]