from django.db import models
from apps.core.models import TimeStampedModel

class Holiday(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.start_date})"

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1
