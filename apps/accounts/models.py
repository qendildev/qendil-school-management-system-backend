from django.db import models
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=[('income', 'Income'), ('expense', 'Expense')])
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Transaction(TimeStampedModel):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(AccountCategory, on_delete=models.RESTRICT, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=20, choices=[('income', 'Income'), ('expense', 'Expense')])
    date = models.DateField()
    description = models.TextField(blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    attachment = models.FileField(upload_to='account_attachments/', null=True, blank=True)
    
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_transactions')

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.type})"

    def save(self, *args, **kwargs):
        # Ensure transaction type matches category type
        if not self.type and self.category:
            self.type = self.category.type
        super().save(*args, **kwargs)
