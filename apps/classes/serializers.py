from rest_framework import serializers
from .models import Class, Section, ClassTeacher
from apps.staff.serializers import StaffProfileSerializer

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        read_only_fields = ('class_name',)

class ClassSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ('id', 'name', 'numeric_name', 'description', 'sections', 'created_at', 'updated_at')

class ClassTeacherSerializer(serializers.ModelSerializer):
    teacher_details = StaffProfileSerializer(source='teacher', read_only=True)
    section_details = SectionSerializer(source='section', read_only=True)

    class Meta:
        model = ClassTeacher
        fields = ('id', 'section', 'teacher', 'teacher_details', 'section_details', 'created_at')

class AssignTeacherSerializer(serializers.Serializer):
    section_id = serializers.IntegerField(required=True)
    teacher_id = serializers.IntegerField(required=True)
