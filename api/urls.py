from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as auth_token
from . import views


app_name = 'api'

urlpatterns = [
    path('api-token-auth/', auth_token.obtain_auth_token),
]

router = routers.SimpleRouter()
router.register('user', views.UserViewSet)
router.register('address', views.AddressViewSet)
router.register('order', views.OrderViewSet)
router.register('orderitem', views.OrderItemViewSet)
urlpatterns += router.urls