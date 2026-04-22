from rest_framework import serializers
from .models import FeeCategory, FeeStructure, FeeInstallment, FeePayment
from apps.classes.serializers import ClassSerializer
from apps.students.serializers import StudentProfileSerializer
from apps.authentication.serializers import UserSerializer

class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = '__all__'

class FeeInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeInstallment
        fields = '__all__'

class FeeStructureSerializer(serializers.ModelSerializer):
    class_details = ClassSerializer(source='class_name', read_only=True)
    category_details = FeeCategorySerializer(source='category', read_only=True)
    installments = FeeInstallmentSerializer(many=True, read_only=True)

    class Meta:
        model = FeeStructure
        fields = '__all__'

class FeePaymentSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    structure_details = FeeStructureSerializer(source='structure', read_only=True)
    collected_by_details = UserSerializer(source='collected_by', read_only=True)

    class Meta:
        model = FeePayment
        fields = '__all__'
        read_only_fields = ('collected_by',)

class SendReminderSerializer(serializers.Serializer):
    student_ids = serializers.ListField(child=serializers.IntegerField())
    message = serializers.CharField()
