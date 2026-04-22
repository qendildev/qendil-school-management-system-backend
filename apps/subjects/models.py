from django.db import models
from apps.core.models import TimeStampedModel
from apps.staff.models import StaffProfile
from apps.classes.models import Class

class Subject(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=[('theory', 'Theory'), ('practical', 'Practical')], default='theory')

    def __str__(self):
        return f"{self.name} ({self.code})"

class SubjectTeacher(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assigned_teachers')
    teacher = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='assigned_subjects')
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subject_teachers')

    class Meta:
        unique_together = ('subject', 'teacher', 'assigned_class')

    def __str__(self):
        return f"{self.subject} - {self.teacher} ({self.assigned_class})"

class Curriculum(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='curriculums')
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='curriculums')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='curriculums/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.subject} ({self.assigned_class})"
