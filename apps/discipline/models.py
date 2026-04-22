from django.db import models
from apps.core.models import TimeStampedModel
from apps.students.models import StudentProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class DisciplineType(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    severity_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('severe', 'Severe')], default='low')

    def __str__(self):
        return self.name

class DisciplineRecord(TimeStampedModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='discipline_records')
    incident_type = models.ForeignKey(DisciplineType, on_delete=models.RESTRICT, related_name='records')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_disciplines')
    action_taken = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')

    def __str__(self):
        return f"{self.student} - {self.title}"
