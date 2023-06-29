from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MessageViewSet


router = DefaultRouter()
router.register("", MessageViewSet, basename="messages")


urlpatterns = [
    path("", include(router.urls))
]
