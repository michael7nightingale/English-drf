from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MessageViewSet, IndexAPIView, CategoryListAPIView, CategoryDetailAPIView
from .views import WordsListAPIView


router = DefaultRouter()
router.register('messages', MessageViewSet, basename='messages')


urlpatterns = [
    path('index/', IndexAPIView.as_view(), name='index'),
    path("categories/", CategoryListAPIView.as_view(), name='category_list'),
    path("categories/<str:category_name>", CategoryDetailAPIView.as_view(), name='category_detail'),
    path("words/<str:category_name>", WordsListAPIView.as_view(), name="words_list"),

]

urlpatterns += router.urls

