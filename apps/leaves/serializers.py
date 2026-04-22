from rest_framework import serializers
from .models import LeaveType, LeaveApplication
from apps.authentication.serializers import UserSerializer

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveApplicationSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    leave_type_details = LeaveTypeSerializer(source='leave_type', read_only=True)
    duration_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveApplication
        fields = '__all__'
        read_only_fields = ('user', 'status', 'approved_by', 'rejection_reason')

class LeaveActionSerializer(serializers.Serializer):
    remarks = serializers.CharField(required=False, allow_blank=True)
