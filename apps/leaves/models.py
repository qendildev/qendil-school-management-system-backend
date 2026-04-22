from django.db import models
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class LeaveType(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    max_days_allowed = models.IntegerField(default=0)
    applicable_for = models.CharField(max_length=20, choices=[('staff', 'Staff'), ('student', 'Student'), ('both', 'Both')], default='both')

    def __str__(self):
        return self.name

class LeaveApplication(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='applications')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    rejection_reason = models.TextField(blank=True)
    attachment = models.FileField(upload_to='leave_attachments/', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.leave_type} ({self.start_date} to {self.end_date})"

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1
