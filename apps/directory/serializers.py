from rest_framework import serializers
from .models import DirectoryContact

class DirectoryContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectoryContact
        fields = '__all__'
