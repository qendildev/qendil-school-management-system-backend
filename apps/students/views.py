from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import StudentProfile, StudentDocument, HealthRecord, AcademicHistory
from .serializers import (
    StudentProfileSerializer, StudentDocumentSerializer, 
    HealthRecordSerializer, AcademicHistorySerializer
)
from apps.core.permissions import IsAdminOrSuperAdmin

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.filter(is_deleted=False)
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete() # uses soft delete
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'put'], url_path='profile')
    def profile(self, request, pk=None):
        student = self.get_object()
        if request.method == 'GET':
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'put'], url_path='health-records')
    def health_records(self, request, pk=None):
        student = self.get_object()
        health_record, created = HealthRecord.objects.get_or_create(student=student)
        
        if request.method == 'GET':
            serializer = HealthRecordSerializer(health_record)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = HealthRecordSerializer(health_record, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='academic-history')
    def academic_history(self, request, pk=None):
        student = self.get_object()
        history = AcademicHistory.objects.filter(student=student)
        serializer = AcademicHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='attendance')
    def attendance(self, request, pk=None):
        return Response({"detail": "Attendance module integration pending."})

    @action(detail=True, methods=['get'], url_path='homework')
    def homework(self, request, pk=None):
        return Response({"detail": "Homework module integration pending."})

    @action(detail=True, methods=['get'], url_path='discipline')
    def discipline(self, request, pk=None):
        return Response({"detail": "Discipline module integration pending."})

class StudentDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentDocumentSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        return StudentDocument.objects.filter(student_id=self.kwargs['student_pk'])

    def perform_create(self, serializer):
        student = get_object_or_404(StudentProfile, pk=self.kwargs['student_pk'])
        serializer.save(student=student)
