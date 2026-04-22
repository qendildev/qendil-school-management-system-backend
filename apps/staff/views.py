from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Department, StaffProfile, StaffPayroll
from .serializers import (
    DepartmentSerializer, StaffProfileSerializer, StaffPayrollSerializer, AssignRoleSerializer
)
from apps.core.permissions import IsAdminOrSuperAdmin

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrSuperAdmin]

class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.filter(is_deleted=False)
    serializer_class = StaffProfileSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete() # uses soft delete
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='assign-role')
    def assign_role(self, request, pk=None):
        staff = self.get_object()
        serializer = AssignRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = staff.user
            user.role = serializer.validated_data['role']
            user.save()
            return Response({"detail": f"Role updated to {user.role}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='attendance')
    def attendance(self, request, pk=None):
        # Placeholder for attendance module integration
        return Response({"detail": "Attendance module integration pending."})

    @action(detail=True, methods=['get'], url_path='leaves')
    def leaves(self, request, pk=None):
        # Placeholder for leaves module integration
        return Response({"detail": "Leaves module integration pending."})

class StaffPayrollViewSet(viewsets.ModelViewSet):
    serializer_class = StaffPayrollSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        return StaffPayroll.objects.filter(staff_id=self.kwargs['staff_pk'])

    def perform_create(self, serializer):
        staff = get_object_or_404(StaffProfile, pk=self.kwargs['staff_pk'])
        serializer.save(staff=staff)
