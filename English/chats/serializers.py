from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    type = serializers.HiddenField(default=Message.NO_REPLY_TYPE)

    class Meta:
        model = Message
        fields = ("id", "user", "reply_to", "text", "type")
