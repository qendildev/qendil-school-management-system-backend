from rest_framework import serializers
from .models import Promotion
from apps.students.serializers import StudentProfileSerializer
from apps.classes.serializers import ClassSerializer, SectionSerializer
from apps.settings_app.serializers import AcademicYearSerializer

class PromotionSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    from_class_details = ClassSerializer(source='from_class', read_only=True)
    to_class_details = ClassSerializer(source='to_class', read_only=True)

    class Meta:
        model = Promotion
        fields = '__all__'

class BulkPromotionSerializer(serializers.Serializer):
    student_ids = serializers.ListField(child=serializers.IntegerField())
    from_class_id = serializers.IntegerField()
    from_section_id = serializers.IntegerField()
    from_academic_year_id = serializers.IntegerField()
    
    to_class_id = serializers.IntegerField()
    to_section_id = serializers.IntegerField()
    to_academic_year_id = serializers.IntegerField()
    
    status = serializers.ChoiceField(choices=[('promoted', 'Promoted'), ('failed', 'Failed'), ('withdrawn', 'Withdrawn')], default='promoted')
    remarks = serializers.CharField(required=False, allow_blank=True)
