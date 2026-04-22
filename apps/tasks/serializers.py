from rest_framework import serializers
from .models import Task
from apps.authentication.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    assigned_by_details = UserSerializer(source='assigned_by', read_only=True)
    assigned_to_details = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('assigned_by',)

class TaskStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
