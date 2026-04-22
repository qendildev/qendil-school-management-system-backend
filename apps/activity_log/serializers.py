from rest_framework import serializers
from .models import ActivityLog
from apps.authentication.serializers import UserSerializer

class ActivityLogSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = ActivityLog
        fields = '__all__'
