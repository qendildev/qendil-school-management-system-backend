from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DisciplineType, DisciplineRecord
from .serializers import DisciplineTypeSerializer, DisciplineRecordSerializer
from apps.core.permissions import IsAdminOrSuperAdmin, IsTeacher

class DisciplineTypeViewSet(viewsets.ModelViewSet):
    queryset = DisciplineType.objects.all()
    serializer_class = DisciplineTypeSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsTeacher]

class DisciplineRecordViewSet(viewsets.ModelViewSet):
    queryset = DisciplineRecord.objects.all()
    serializer_class = DisciplineRecordSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsTeacher]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

    @action(detail=False, methods=['get'], url_path=r'by-student/(?P<student_id>\d+)')
    def by_student(self, request, student_id=None):
        records = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='reports')
    def reports(self, request):
        return Response({"detail": "Discipline reports logic pending."})
