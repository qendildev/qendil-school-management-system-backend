from django.db import models
from apps.core.models import TimeStampedModel
from apps.classes.models import Class

class Admission(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('converted', 'Converted to Student'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    
    parent_name = models.CharField(max_length=200)
    parent_phone = models.CharField(max_length=20)
    parent_email = models.EmailField(blank=True)
    
    applied_for_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='admissions')
    previous_school = models.CharField(max_length=200, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.applied_for_class}"

class AdmissionDocument(TimeStampedModel):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='admission_documents/')

    def __str__(self):
        return f"{self.title} - {self.admission.first_name}"
