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
    grade = serializers.IntegerField(source='numeric_name', required=False, allow_null=True)
    capacity = serializers.IntegerField(write_only=True, required=False, default=30)

    class Meta:
        model = Class
        fields = ('id', 'name', 'grade', 'numeric_name', 'description', 'sections', 'capacity', 'created_at', 'updated_at')
        extra_kwargs = {
            'numeric_name': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        capacity = validated_data.pop('capacity', 30)
        class_obj = super().create(validated_data)
        
        # Automatically create a default Section A for the new class
        Section.objects.create(
            class_name=class_obj,
            name="A",
            capacity=capacity
        )
        return class_obj

class ClassTeacherSerializer(serializers.ModelSerializer):
    teacher_details = StaffProfileSerializer(source='teacher', read_only=True)
    section_details = SectionSerializer(source='section', read_only=True)

    class Meta:
        model = ClassTeacher
        fields = ('id', 'section', 'teacher', 'teacher_details', 'section_details', 'created_at')

class AssignTeacherSerializer(serializers.Serializer):
    section_id = serializers.IntegerField(required=True)
    teacher_id = serializers.IntegerField(required=True)
