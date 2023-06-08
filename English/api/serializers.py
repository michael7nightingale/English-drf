from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ("id", "user", "reply_to", "text", "type")

