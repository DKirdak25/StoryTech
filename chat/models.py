from django.db import models

class ChatSession(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # NEW
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.session_id

class Message(models.Model):
    chat = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("admin", "Admin")])
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:20]}"