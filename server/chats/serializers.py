from rest_framework import serializers

from .models import Message, Chat
from users.serializers import AccountShortDetailSerializer


class MessageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ("sender", "reply_to", "text", "type", "time_send")


class MessageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ("sender", "reply_to", "text", "type", "time_send")


class ChatRetrieveSerializer(serializers.ModelSerializer):
    messages = MessageListSerializer(many=True, read_only=True)
    account = AccountShortDetailSerializer()
    chat_gpt_account = AccountShortDetailSerializer()

    class Meta:
        model = Chat
        fields = ("chat_gpt_account", "account", "messages")



