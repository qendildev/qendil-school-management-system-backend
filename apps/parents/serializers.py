from rest_framework import serializers
from .models import ParentProfile, ParentStudentLink
from apps.authentication.serializers import UserSerializer
from apps.students.serializers import StudentProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ParentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )

    class Meta:
        model = ParentProfile
        fields = '__all__'

class ParentStudentLinkSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)

    class Meta:
        model = ParentStudentLink
        fields = ('id', 'student', 'relationship', 'created_at')

class LinkStudentSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(required=True)
    relationship = serializers.ChoiceField(choices=[('father', 'Father'), ('mother', 'Mother'), ('guardian', 'Guardian')])
