from django.urls import path, re_path,include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
# router.register("users", UserViewSet, basename='users')


urlpatterns = [
    re_path(r'auth/', include('djoser.urls')),
    re_path(r"^auth/", include("djoser.urls.authtoken")),

]

urlpatterns += router.urls
