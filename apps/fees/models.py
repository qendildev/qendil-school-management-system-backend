from django.db import models
from apps.core.models import TimeStampedModel
from apps.classes.models import Class
from apps.students.models import StudentProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class FeeCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class FeeStructure(TimeStampedModel):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='fee_structures')
    category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE, related_name='structures')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    academic_year = models.CharField(max_length=20) # e.g. "2023-2024"
    frequency = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('termly', 'Termly'), ('annually', 'Annually'), ('one_time', 'One Time')])
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('class_name', 'category', 'academic_year')

    def __str__(self):
        return f"{self.class_name} - {self.category} ({self.academic_year})"

class FeeInstallment(TimeStampedModel):
    structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='installments')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.structure} - {self.title}"

class FeePayment(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Gateway'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='fee_payments')
    structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True, related_name='payments')
    installment = models.ForeignKey(FeeInstallment, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='cash')
    reference_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    remarks = models.TextField(blank=True)
    
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='collected_fees')

    def __str__(self):
        return f"{self.student} - {self.amount_paid} on {self.payment_date}"
