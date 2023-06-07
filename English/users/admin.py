from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email')

