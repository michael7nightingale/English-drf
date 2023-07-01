from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions, status, generics

from .serializers import MessageListSerializer, MessageDetailSerializer
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
    serializer_class = MessageListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "chat_id"

    def retrieve(self, request, *args, **kwargs):
        chat_id = kwargs[self.lookup_url_kwarg]
        chat = request.user.account.chat
        if chat.id == chat_id:
            messages = Message.objects.filter(chat=chat)
            serializer = self.serializer_class(insatance=messages, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "No permission to watch this data."}, status=status.HTTP_403_FORBIDDEN)
