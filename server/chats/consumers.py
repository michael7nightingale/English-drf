import json
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
import redis

from services.ai.messenger import Messenger
from .models import Chat, Message


redis_connection = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)


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

        if text == "Generate":
            await self.generate_pupil_message()
        else:
            last_message_json = redis_connection.get(str(self.account.id))
            last_message = json.loads(last_message_json)
            if last_message is None:
                await self.answer_remark_message(text)
            else:
                if last_message['type'] == 'pupil':
                    await self.answer_pupil_message(text)
                elif last_message['type'] == 'remark':
                    await self.answer_remark_message(text)
                else:
                    await self.send(text_data=json.dumps({'text': "Unknown message type."}))

    async def generate_pupil_message(self):
        new_message = Messenger.generate(self.chat)
        redis_connection.set(
            str(self.account.id),
            {"text": new_message.text, "type": new_message.type}
        )
        await self.send(text_data=json.dumps({'text': new_message.text}))

    async def answer_pupil_message(self, text):
        new_message = Message.objects.create(
            sender=self.account,
            chat=self.chat,
            text=text,
            type="pupil"
        )
        await self.send(text_data=json.dumps({'text': new_message.text}))

        pupil_answer_message = Messenger(new_message).chat()
        await self.send(text_data=json.dumps({'text': pupil_answer_message.text}))
        redis_connection.set(str(self.account.id), None)

    async def answer_remark_message(self, text):
        new_message = Message.objects.create(
            sender=self.account,
            chat=self.chat,
            text=text,
            type="remark"
        )
        await self.send(text_data=json.dumps({'text': new_message.text}))

        answer_message = Messenger(new_message).chat()
        await self.send(text_data=json.dumps({'text': answer_message.text}))

    # async def send_remark_message(self, text):
    #     new_message = Message.objects.create(
    #         sender=self.account,
    #         chat=self.chat,
    #         text=text,
    #         type="remark"
    #     )
    #     return new_message
