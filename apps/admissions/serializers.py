from rest_framework import serializers
from .models import Admission, AdmissionDocument
from apps.classes.serializers import ClassSerializer

class AdmissionDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionDocument
        fields = '__all__'
        read_only_fields = ('admission',)

class AdmissionSerializer(serializers.ModelSerializer):
    applied_for_class_details = ClassSerializer(source='applied_for_class', read_only=True)
    documents = AdmissionDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Admission
        fields = '__all__'

class AdmissionStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Admission.STATUS_CHOICES)
    remarks = serializers.CharField(allow_blank=True, required=False)

class ConvertToStudentSerializer(serializers.Serializer):
    admission_number = serializers.CharField(required=True)
