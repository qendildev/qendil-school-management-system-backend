from rest_framework import serializers
from .models import DisciplineType, DisciplineRecord
from apps.students.serializers import StudentProfileSerializer
from apps.authentication.serializers import UserSerializer

class DisciplineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplineType
        fields = '__all__'

class DisciplineRecordSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    incident_type_details = DisciplineTypeSerializer(source='incident_type', read_only=True)
    reported_by_details = UserSerializer(source='reported_by', read_only=True)

    class Meta:
        model = DisciplineRecord
        fields = '__all__'
        read_only_fields = ('reported_by',)
