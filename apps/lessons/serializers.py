from rest_framework import serializers
from .models import Lesson, Timetable
from apps.classes.serializers import ClassSerializer, SectionSerializer
from apps.subjects.serializers import SubjectSerializer
from apps.staff.serializers import StaffProfileSerializer

class LessonSerializer(serializers.ModelSerializer):
    class_details = ClassSerializer(source='class_name', read_only=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)
    teacher_details = StaffProfileSerializer(source='teacher', read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'

class TimetableSerializer(serializers.ModelSerializer):
    class_details = ClassSerializer(source='class_name', read_only=True)
    section_details = SectionSerializer(source='section', read_only=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)
    teacher_details = StaffProfileSerializer(source='teacher', read_only=True)

    class Meta:
        model = Timetable
        fields = '__all__'
