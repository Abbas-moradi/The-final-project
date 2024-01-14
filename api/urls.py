from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import views


app_name = 'api'

urlpatterns = [
    path('api-token-auth/', auth_token.obtain_auth_token),
    path('comment/', views.CommentView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

router = routers.SimpleRouter()
router.register('user', views.UserViewSet)
router.register('address', views.AddressViewSet)
router.register('order', views.OrderViewSet)
urlpatterns += router.urls