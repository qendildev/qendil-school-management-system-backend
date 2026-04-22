from django.db import models
from apps.core.models import TimeStampedModel
from apps.classes.models import Class, Section
from apps.subjects.models import Subject
from apps.staff.models import StaffProfile
from apps.students.models import StudentProfile

class Homework(TimeStampedModel):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='homeworks')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='homeworks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='homeworks_given')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_date = models.DateField()
    due_date = models.DateField()
    file = models.FileField(upload_to='homeworks/', null=True, blank=True)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.title} - {self.subject} ({self.class_name})"

class HomeworkSubmission(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late'),
    ]

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='homework_submissions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(null=True, blank=True)
    file = models.FileField(upload_to='homework_submissions/', null=True, blank=True)
    remarks = models.TextField(blank=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('homework', 'student')

    def __str__(self):
        return f"{self.homework.title} - {self.student}"
