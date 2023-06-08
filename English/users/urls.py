from django.urls import path, re_path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

from .views import *


router = DefaultRouter()
# router.register("users", UserViewSet, basename='users')


urlpatterns = [
    path('auth/', include(
        [
            path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
            path("token/verify/", TokenVerifyView.as_view(), name='token_verify')
        ]
    )),



]

urlpatterns += router.urls
