from rest_framework import serializers

from .models import Message, Category, Word


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    type = serializers.HiddenField(default=Message.NO_REPLY_TYPE)

    class Meta:
        model = Message
        fields = ("id", "user", "reply_to", "text", "type")


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    url = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    title = serializers.CharField(max_length=100)
    count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'url', 'count')


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = "__all__"
