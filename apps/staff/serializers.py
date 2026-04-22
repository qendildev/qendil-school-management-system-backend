from rest_framework import serializers
from .models import Department, StaffProfile, StaffPayroll
from apps.authentication.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), write_only=True, source='department', required=False, allow_null=True
    )

    class Meta:
        model = StaffProfile
        fields = '__all__'

class StaffPayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPayroll
        fields = '__all__'
        read_only_fields = ('staff',)

class AssignRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
