from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import StudentAttendance, StaffAttendance
from apps.students.models import StudentProfile
from apps.classes.models import Class, Section
from .serializers import (
    StudentAttendanceSerializer, StaffAttendanceSerializer, BulkStudentAttendanceSerializer
)
from apps.core.permissions import IsAdminOrSuperAdmin, IsTeacher

class StudentAttendanceViewSet(viewsets.ModelViewSet):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsTeacher]

    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk(self, request):
        serializer = BulkStudentAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            class_id = serializer.validated_data['class_id']
            section_id = serializer.validated_data['section_id']
            date = serializer.validated_data['date']
            students_data = serializer.validated_data['students']

            class_obj = get_object_or_404(Class, pk=class_id)
            section_obj = get_object_or_404(Section, pk=section_id)

            created_count = 0
            updated_count = 0

            for s_data in students_data:
                student = get_object_or_404(StudentProfile, pk=s_data['student_id'])
                att, created = StudentAttendance.objects.get_or_create(
                    student=student,
                    date=date,
                    defaults={
                        'class_name': class_obj,
                        'section': section_obj,
                        'status': s_data['status'],
                        'remark': s_data.get('remark', '')
                    }
                )
                if not created:
                    att.status = s_data['status']
                    att.remark = s_data.get('remark', '')
                    att.save()
                    updated_count += 1
                else:
                    created_count += 1

            return Response({
                "detail": f"Bulk attendance recorded. Created: {created_count}, Updated: {updated_count}"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path=r'by-class/(?P<class_id>\d+)')
    def by_class(self, request, class_id=None):
        date = request.query_params.get('date')
        queryset = self.queryset.filter(class_name_id=class_id)
        if date:
            queryset = queryset.filter(date=date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-date')
    def by_date(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response({"detail": "date query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.queryset.filter(date=date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='report')
    def report(self, request):
        return Response({"detail": "Student attendance report not implemented yet."})

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        return Response({"detail": "Student attendance summary not implemented yet."})

class StaffAttendanceViewSet(viewsets.ModelViewSet):
    queryset = StaffAttendance.objects.all()
    serializer_class = StaffAttendanceSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    @action(detail=False, methods=['get'], url_path='report')
    def report(self, request):
        return Response({"detail": "Staff attendance report not implemented yet."})
