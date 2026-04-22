from django.db import models
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from apps.staff.models import StaffProfile

User = get_user_model()

class Class(TimeStampedModel):
    name = models.CharField(max_length=50) # e.g. "Grade 1"
    numeric_name = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Section(TimeStampedModel):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=50) # e.g. "A"
    capacity = models.IntegerField(default=30)
    
    class Meta:
        unique_together = ('class_name', 'name')

    def __str__(self):
        return f"{self.class_name.name} - {self.name}"

class ClassTeacher(TimeStampedModel):
    section = models.OneToOneField(Section, on_delete=models.CASCADE, related_name='class_teacher')
    teacher = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='assigned_sections')
    
    def __str__(self):
        return f"{self.section} - {self.teacher}"
