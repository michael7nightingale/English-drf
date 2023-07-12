import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import cache

from services.ai.messenger import Messenger
from .models import Chat, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.account = self.scope['user'].account
        self.chat = self.account.chat
        self.chat_id = str(self.chat.id)

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
    async def receive(self, text_data):
        text_data = json.loads(text_data)
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
            last_message_json = cache.get(self.account.id)
            if last_message_json is None:
                await self.answer_remark_message(text)
            else:
                last_message = last_message_json
                if last_message['type'] == 'pupil':
                    await self.answer_pupil_message(text, last_message)
                elif last_message['type'] == 'remark':
                    await self.answer_remark_message(text)
                else:
                    await self.send(text_data=json.dumps({'text': "Unknown message type."}))

    async def generate_pupil_message(self):
        new_message = await sync_to_async(Messenger.generate)(self.chat)
        print(12312, new_message)
        cache.set(
            self.account.id,
            {"text": new_message.text, "type": new_message.type}
        )
        await self.send(text_data=json.dumps({'text': new_message.text}))

    async def answer_pupil_message(self, text, last_message):
        new_message = await sync_to_async(Message.objects.create)(
            sender=self.account,
            chat=self.chat,
            text=text,
            type="pupil"
        )
        await self.send(text_data=json.dumps({'text': new_message.text}))

        pupil_answer_message = await sync_to_async(Messenger(new_message).chat)(last_message)
        await self.send(text_data=json.dumps({'text': pupil_answer_message.text}))
        cache.set(self.account.id, None)

    async def answer_remark_message(self, text):
        new_message = await sync_to_async(Message.objects.create)(
            sender=self.account,
            chat=self.chat,
            text=text,
            type="remark"
        )
        await self.send(text_data=json.dumps({'text': new_message.text}))

        answer_message = await sync_to_async(Messenger(new_message).chat)()
        await self.send(text_data=json.dumps({'text': answer_message.text}))

    # async def send_remark_message(self, text):
    #     new_message = Message.objects.create(
    #         sender=self.account,
    #         chat=self.chat,
    #         text=text,
    #         type="remark"
    #     )
    #     return new_message
