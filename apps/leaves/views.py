from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import LeaveType, LeaveApplication
from .serializers import LeaveTypeSerializer, LeaveApplicationSerializer, LeaveActionSerializer
from apps.core.permissions import IsAdminOrSuperAdmin

class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAdminOrSuperAdmin]

class LeaveApplicationViewSet(viewsets.ModelViewSet):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['put'], url_path='approve')
    def approve(self, request, pk=None):
        leave = self.get_object()
        if not request.user.role in ['admin', 'superadmin']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        leave.status = 'approved'
        leave.approved_by = request.user
        leave.save()
        return Response({"detail": "Leave application approved."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_path='reject')
    def reject(self, request, pk=None):
        leave = self.get_object()
        if not request.user.role in ['admin', 'superadmin']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LeaveActionSerializer(data=request.data)
        if serializer.is_valid():
            leave.status = 'rejected'
            leave.approved_by = request.user
            leave.rejection_reason = serializer.validated_data.get('remarks', '')
            leave.save()
            return Response({"detail": "Leave application rejected."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='staff')
    def staff_leaves(self, request):
        leaves = self.queryset.filter(user__role__in=['teacher', 'admin', 'librarian', 'accountant'])
        serializer = self.get_serializer(leaves, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='students')
    def student_leaves(self, request):
        leaves = self.queryset.filter(user__role='student')
        serializer = self.get_serializer(leaves, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='pending')
    def pending_leaves(self, request):
        leaves = self.queryset.filter(status='pending')
        serializer = self.get_serializer(leaves, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'balance/(?P<user_id>\d+)')
    def leave_balance(self, request, user_id=None):
        # Placeholder for leave balance logic
        return Response({"detail": "Leave balance logic pending."})
    
    # Alias to match requested path /api/leaves/balance/{staff_id}/
    @action(detail=False, methods=['get'], url_path=r'balance/(?P<staff_id>\d+)')
    def staff_leave_balance(self, request, staff_id=None):
        return self.leave_balance(request, staff_id)
