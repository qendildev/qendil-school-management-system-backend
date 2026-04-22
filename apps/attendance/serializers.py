from rest_framework import serializers
from .models import StudentAttendance, StaffAttendance
from apps.students.serializers import StudentProfileSerializer
from apps.staff.serializers import StaffProfileSerializer

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'

class StaffAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAttendance
        fields = '__all__'

class BulkStudentAttendanceSerializer(serializers.Serializer):
    class_id = serializers.IntegerField(required=True)
    section_id = serializers.IntegerField(required=True)
    date = serializers.DateField(required=True)
    students = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    # expected students format: [{"student_id": 1, "status": "present", "remark": ""}, ...]
