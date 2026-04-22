from rest_framework import serializers
from .models import Notification, Message
from apps.authentication.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender_details = UserSerializer(source='sender', read_only=True)
    recipient_details = UserSerializer(source='recipient', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender', 'status')

class BulkNotificationSerializer(serializers.Serializer):
    recipient_ids = serializers.ListField(child=serializers.IntegerField())
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    notification_type = serializers.CharField(max_length=50, required=False)

class SendCommunicationSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()
    subject = serializers.CharField(max_length=255)
    body = serializers.CharField()
