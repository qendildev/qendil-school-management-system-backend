from rest_framework import serializers
from .models import Subject, SubjectTeacher, Curriculum
from apps.staff.serializers import StaffProfileSerializer
from apps.classes.serializers import ClassSerializer

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectTeacherSerializer(serializers.ModelSerializer):
    teacher_details = StaffProfileSerializer(source='teacher', read_only=True)
    class_details = ClassSerializer(source='assigned_class', read_only=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)

    class Meta:
        model = SubjectTeacher
        fields = ('id', 'subject', 'teacher', 'assigned_class', 'teacher_details', 'class_details', 'subject_details', 'created_at')

class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'

class AssignTeacherToSubjectSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField(required=True)
    assigned_class_id = serializers.IntegerField(required=True)
