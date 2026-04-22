from django.db import models
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Notice(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices')
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    
    # Target audience
    target_roles = models.JSONField(default=list, blank=True) # e.g. ["student", "teacher"]
    
    def __str__(self):
        return self.title
