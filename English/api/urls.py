from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MessageViewSet, IndexAPIView

router = DefaultRouter()
router.register('messages', MessageViewSet, basename='messages')


urlpatterns = [
    path('index/', IndexAPIView.as_view(), name='index'),

]

urlpatterns += router.urls

