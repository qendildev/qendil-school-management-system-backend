from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from apps.core.permissions import IsAdminOrSuperAdmin

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Activity logs are read-only via the API.
    They are created via Django signals.
    """
    queryset = ActivityLog.objects.all().order_by('-created_at')
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    @action(detail=False, methods=['get'], url_path=r'by-user/(?P<user_id>\d+)')
    def by_user(self, request, user_id=None):
        logs = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-module')
    def by_module(self, request):
        module_name = request.query_params.get('module')
        if not module_name:
            return Response({"detail": "module parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        logs = self.queryset.filter(module__icontains=module_name)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_logs(self, request):
        if request.user.role != 'superadmin':
            return Response({"detail": "Only Superadmin can clear logs."}, status=status.HTTP_403_FORBIDDEN)
        
        count, _ = self.queryset.delete()
        return Response({"detail": f"Cleared {count} activity logs."}, status=status.HTTP_200_OK)
