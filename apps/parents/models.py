from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.students.models import StudentProfile

User = get_user_model()

class ParentProfile(TimeStampedModel, SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    occupation = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    alternate_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class ParentStudentLink(TimeStampedModel):
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='student_links')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='parent_links')
    relationship = models.CharField(max_length=50, choices=[('father', 'Father'), ('mother', 'Mother'), ('guardian', 'Guardian')])

    class Meta:
        unique_together = ('parent', 'student')

    def __str__(self):
        return f"{self.parent} -> {self.student}"
