import json
from django.http.response import HttpResponseNotAllowed
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat = Chat.objects.create(self.chat_id)
        self.account = self.scope['user'].account
        # Join room group
        await self.channel_layer.group_add(
            self.chat_id, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_id, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, json_data):
        text_data = json.loads(json_data)
        text = text_data["text"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_id, {"type": "chat_message", "text": text}
        )

    async def chat_message(self, event):
        """Resend message to websocket."""
        text = event["text"]
        new_message = Message.objects.create(
            sender=self.account,
            chat=self.chat,
            text=text,
        )

        await self.send(text_data=json.dumps({"text": new_message.text}))
