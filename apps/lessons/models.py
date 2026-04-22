from django.db import models
from apps.core.models import TimeStampedModel
from apps.classes.models import Class, Section
from apps.subjects.models import Subject
from apps.staff.models import StaffProfile

class Lesson(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='lessons')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='lessons')
    file = models.FileField(upload_to='lessons/', null=True, blank=True)
    video_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.subject} ({self.class_name})"

class Timetable(TimeStampedModel):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='timetables')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='timetables')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetables')
    teacher = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='timetables')
    
    day_of_week = models.CharField(max_length=15, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=50, blank=True)

    class Meta:
        # Prevent double booking a teacher or a section at the exact same time/day
        # This is a basic unique constraint, more complex overlapping validation would go in clean()
        unique_together = (('teacher', 'day_of_week', 'start_time'), ('section', 'day_of_week', 'start_time'))

    def __str__(self):
        return f"{self.class_name} - {self.subject} ({self.day_of_week} {self.start_time})"
