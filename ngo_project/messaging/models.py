from django.db import models
from accounts.models import CustomUser  # Import Custom User model
from django.utils.timezone import now

class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_admin = models.BooleanField(default=False)
    sent_at = models.DateTimeField(default=now)

    def __str__(self):
        sender = "Admin" if self.is_admin else self.user.email
        return f"{sender}: {self.message[:50]}..."
