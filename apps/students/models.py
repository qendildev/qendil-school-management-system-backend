from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.settings_app.models import AcademicYear

User = get_user_model()

class StudentProfile(TimeStampedModel, SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=50, unique=True)
    roll_number = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    
    # Class and Section relations will be linked through the classes module 
    # but we keep a generic active academic year ref here if needed.
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"

class StudentDocument(TimeStampedModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to='student_documents/')
    
    def __str__(self):
        return f"{self.title} - {self.student.admission_number}"

class HealthRecord(TimeStampedModel):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='health_record')
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # in kg
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    regular_medications = models.TextField(blank=True)
    physician_name = models.CharField(max_length=100, blank=True)
    physician_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Health Record - {self.student.admission_number}"

class AcademicHistory(TimeStampedModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='academic_histories')
    previous_school = models.CharField(max_length=200)
    year_attended = models.CharField(max_length=50)
    grade_completed = models.CharField(max_length=50)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.previous_school} - {self.student.admission_number}"
