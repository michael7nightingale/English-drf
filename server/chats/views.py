from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions, status, generics

from .serializers import MessageListSerializer, MessageDetailSerializer, ChatRetrieveSerializer
from .models import Message
from services.ai.messenger import Messenger


class MessageGenerateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageDetailSerializer

    def create(self, request, *args, **kwargs):
        generated_message = Messenger.generate()
        serializer = self.serializer_class(generated_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatAPIView(generics.RetrieveAPIView):
    serializer_class = ChatRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        chat = request.user.account.chat
        # messages = Message.objects.filter(chat=chat)
        serializer = self.serializer_class(insatance=chat, many=True)
        return Response(serializer.data)
