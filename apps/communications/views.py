from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Notification, Message
from .serializers import (
    NotificationSerializer, MessageSerializer, 
    BulkNotificationSerializer, SendCommunicationSerializer
)
from apps.core.permissions import IsAdminOrSuperAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own notifications
        return self.queryset.filter(recipient=self.request.user)

    @action(detail=True, methods=['put'], url_path='read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({"detail": "All notifications marked as read."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='send-bulk')
    def send_bulk(self, request):
        if not request.user.role in ['admin', 'superadmin']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BulkNotificationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            recipients = User.objects.filter(id__in=data['recipient_ids'])
            
            notifications = [
                Notification(
                    recipient=user,
                    title=data['title'],
                    message=data['message'],
                    notification_type=data.get('notification_type', 'system')
                ) for user in recipients
            ]
            
            Notification.objects.bulk_create(notifications)
            return Response({"detail": f"Sent {len(notifications)} notifications."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommunicationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='inbox')
    def inbox(self, request):
        messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sent')
    def sent(self, request):
        messages = Message.objects.filter(sender=request.user).order_by('-created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='email/send')
    def send_email(self, request):
        if not request.user.role in ['admin', 'superadmin']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = SendCommunicationSerializer(data=request.data)
        if serializer.is_valid():
            # Placeholder for actual email sending logic (e.g. send_mail)
            data = serializer.validated_data
            recipient = get_object_or_404(User, pk=data['recipient_id'])
            
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                subject=data['subject'],
                body=data['body'],
                sent_via='email'
            )
            return Response({"detail": "Email sent (placeholder logic)."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='sms/send')
    def send_sms(self, request):
        if not request.user.role in ['admin', 'superadmin']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = SendCommunicationSerializer(data=request.data)
        if serializer.is_valid():
            # Placeholder for actual SMS sending logic (e.g. Twilio)
            data = serializer.validated_data
            recipient = get_object_or_404(User, pk=data['recipient_id'])
            
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                subject=data['subject'],
                body=data['body'],
                sent_via='sms'
            )
            return Response({"detail": "SMS sent (placeholder logic)."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
