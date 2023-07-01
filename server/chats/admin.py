from django.contrib import admin

from .models import Chat, Message


@admin.register(Chat)
class Chat(admin.ModelAdmin):
    list_display = ('id', "account")


@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = ('id', "chat", 'type', "sender")
