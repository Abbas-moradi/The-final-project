from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_token
from rest_framework import routers


app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UsreLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('address/', views.UserAddress.as_view(), name='user_address'),
    path('edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('my_order/', views.MyOrder.as_view(), name='my_order'),
    path('user/', views.UserCreateView.as_view(), name='user-list-create'),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', auth_token.obtain_auth_token),
]

router = routers.SimpleRouter()
router.register('user', views.UserViewSet)
urlpatterns += router.urls