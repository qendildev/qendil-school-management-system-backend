from rest_framework import serializers
from .models import Notice
from apps.authentication.serializers import UserSerializer

class NoticeSerializer(serializers.ModelSerializer):
    author_details = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ('author', 'is_published', 'publish_date')
