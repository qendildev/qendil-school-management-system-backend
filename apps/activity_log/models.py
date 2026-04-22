from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()

class ActivityLog(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activity_logs')
    action = models.CharField(max_length=255) # e.g. "Created", "Updated", "Deleted"
    module = models.CharField(max_length=100) # e.g. "Students", "Homework"
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} ({self.object_id})"
