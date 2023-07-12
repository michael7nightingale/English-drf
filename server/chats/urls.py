from django.urls import path

from .views import ChatAPIView, chat_view, room_view


urlpatterns = [
    path("", ChatAPIView.as_view(), name='chats_detail'),
    # template views for websockets
    path("chat-html/", chat_view, name="chat_view"),
    path("room-html/", room_view, name="room_view"),

]
