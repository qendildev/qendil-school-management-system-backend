from rest_framework import serializers
from .models import AccountCategory, Transaction
from apps.authentication.serializers import UserSerializer

class AccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountCategory
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    category_details = AccountCategorySerializer(source='category', read_only=True)
    recorded_by_details = UserSerializer(source='recorded_by', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('recorded_by',)
