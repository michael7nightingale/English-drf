from django.urls import path

from .views import ChatAPIView


urlpatterns = [
    path("<str:chat_id>/", ChatAPIView.as_view(), name='chats_detail'),

]
