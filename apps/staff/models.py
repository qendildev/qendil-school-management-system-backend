from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel, SoftDeleteModel

User = get_user_model()

class Department(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')

    def __str__(self):
        return self.name

class StaffProfile(TimeStampedModel, SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()
    qualification = models.CharField(max_length=200, blank=True)
    experience_details = models.TextField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=50, blank=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bank_account_details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"

class StaffPayroll(TimeStampedModel):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='payrolls')
    month = models.IntegerField()
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')

    class Meta:
        unique_together = ('staff', 'month', 'year')

    def __str__(self):
        return f"{self.staff.user.username} - {self.month}/{self.year}"
