from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as auth_token
from . import views


app_name = 'api'

urlpatterns = [

]

router = routers.SimpleRouter()
router.register('user', views.UserViewSet)
urlpatterns += router.urls