from django.db import models
from apps.core.models import TimeStampedModel

class DirectoryContact(TimeStampedModel):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100) # e.g. "Vendor", "Emergency", "Staff"
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
