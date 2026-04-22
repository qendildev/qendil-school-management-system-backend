from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Notice
from .serializers import NoticeSerializer
from apps.core.permissions import IsAdminOrSuperAdmin

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'active', 'by_role']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrSuperAdmin()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        notice = self.get_object()
        notice.is_published = True
        notice.publish_date = timezone.now()
        notice.save()
        return Response({"detail": "Notice published."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unpublish')
    def unpublish(self, request, pk=None):
        notice = self.get_object()
        notice.is_published = False
        notice.save()
        return Response({"detail": "Notice unpublished."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='active')
    def active(self, request):
        notices = self.queryset.filter(is_published=True).order_by('-publish_date')
        # Filter by user role if not admin
        if not request.user.role in ['admin', 'superadmin']:
            # Using JSONField __contains logic
            notices = notices.filter(target_roles__contains=request.user.role)
        
        serializer = self.get_serializer(notices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-role')
    def by_role(self, request):
        role = request.query_params.get('role')
        if not role:
            return Response({"detail": "role parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        notices = self.queryset.filter(target_roles__contains=role).order_by('-publish_date')
        serializer = self.get_serializer(notices, many=True)
        return Response(serializer.data)
