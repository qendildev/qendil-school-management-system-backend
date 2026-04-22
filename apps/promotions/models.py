from django.db import models
from apps.core.models import TimeStampedModel
from apps.students.models import StudentProfile
from apps.classes.models import Class, Section
from apps.settings_app.models import AcademicYear

class Promotion(TimeStampedModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='promotions')
    
    from_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='promotions_from')
    from_section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='promotions_from')
    from_academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='promotions_from')
    
    to_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='promotions_to')
    to_section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='promotions_to')
    to_academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='promotions_to')
    
    promotion_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('promoted', 'Promoted'), ('failed', 'Failed'), ('withdrawn', 'Withdrawn')], default='promoted')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} promoted to {self.to_class}"
