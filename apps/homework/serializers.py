from rest_framework import serializers
from .models import Homework, HomeworkSubmission
from apps.classes.serializers import ClassSerializer, SectionSerializer
from apps.subjects.serializers import SubjectSerializer
from apps.staff.serializers import StaffProfileSerializer
from apps.students.serializers import StudentProfileSerializer

class HomeworkSerializer(serializers.ModelSerializer):
    class_details = ClassSerializer(source='class_name', read_only=True)
    section_details = SectionSerializer(source='section', read_only=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)
    teacher_details = StaffProfileSerializer(source='teacher', read_only=True)

    class Meta:
        model = Homework
        fields = '__all__'

class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)

    class Meta:
        model = HomeworkSubmission
        fields = '__all__'
        read_only_fields = ('homework',)

class GradeSubmissionSerializer(serializers.Serializer):
    marks_obtained = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    remarks = serializers.CharField(allow_blank=True, required=False)
