from django.contrib import admin
from .models import Chat, ChatMessage

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
	list_display = ('id', 'user1', 'user2', 'created')

@admin.register(ChatMessage)	
class ChatMessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'message', 'chat', 'created')