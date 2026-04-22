from django.db import models
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(TimeStampedModel):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, blank=True) # e.g. 'homework', 'attendance', 'system'
    
    def __str__(self):
        return f"{self.recipient} - {self.title}"

class Message(TimeStampedModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    
    # For email/sms tracking
    sent_via = models.CharField(max_length=20, choices=[('in_app', 'In-App'), ('email', 'Email'), ('sms', 'SMS')], default='in_app')
    status = models.CharField(max_length=20, default='sent')

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.subject}"
