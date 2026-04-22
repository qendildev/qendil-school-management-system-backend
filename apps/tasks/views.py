from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer, TaskStatusSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('due_date')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Default to tasks assigned to or by the user, unless admin
        if self.request.user.role in ['admin', 'superadmin']:
            return self.queryset
        return self.queryset.filter(assigned_to=self.request.user) | self.queryset.filter(assigned_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    @action(detail=True, methods=['put'], url_path='status')
    def change_status(self, request, pk=None):
        task = self.get_object()
        # Only assignee, assigner, or admin can change status
        if request.user != task.assigned_to and request.user != task.assigned_by and request.user.role not in ['admin', 'superadmin']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = TaskStatusSerializer(data=request.data)
        if serializer.is_valid():
            task.status = serializer.validated_data['status']
            task.save()
            return Response({"detail": "Status updated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='assigned-to-me')
    def assigned_to_me(self, request):
        tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='assigned-by-me')
    def assigned_by_me(self, request):
        tasks = Task.objects.filter(assigned_by=request.user).order_by('due_date')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue(self, request):
        now = timezone.now()
        tasks = self.get_queryset().filter(due_date__lt=now).exclude(status__in=['completed', 'cancelled'])
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
