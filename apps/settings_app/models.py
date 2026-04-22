from django.db import models
from apps.core.models import TimeStampedModel

class SchoolInfo(TimeStampedModel):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='school_logos/', null=True, blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # Ensure only one SchoolInfo instance exists
        if not self.pk and SchoolInfo.objects.exists():
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class AcademicYear(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True) # e.g. "2023-2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class GeneralSettings(TimeStampedModel):
    currency_symbol = models.CharField(max_length=10, default='$')
    timezone = models.CharField(max_length=100, default='UTC')
    date_format = models.CharField(max_length=50, default='YYYY-MM-DD')
    language = models.CharField(max_length=20, default='en')
    
    def save(self, *args, **kwargs):
        # Ensure only one GeneralSettings instance exists
        if not self.pk and GeneralSettings.objects.exists():
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return "General Settings"

class Permission(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Role(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')

    def __str__(self):
        return self.name
