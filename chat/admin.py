from django.contrib import admin
from .models import ChatSession, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    fields = ("sender", "text")
    can_delete = False

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("name", "session_id", "created_at")
    inlines = [MessageInline]
