from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Admission, AdmissionDocument
from .serializers import (
    AdmissionSerializer, AdmissionDocumentSerializer, 
    AdmissionStatusSerializer, ConvertToStudentSerializer
)
from apps.students.models import StudentProfile
from apps.core.permissions import IsAdminOrSuperAdmin

User = get_user_model()

class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    @action(detail=True, methods=['put'], url_path='status')
    def change_status(self, request, pk=None):
        admission = self.get_object()
        serializer = AdmissionStatusSerializer(data=request.data)
        if serializer.is_valid():
            admission.status = serializer.validated_data['status']
            admission.remarks = serializer.validated_data.get('remarks', admission.remarks)
            admission.save()
            return Response({"detail": f"Status updated to {admission.status}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        admissions = self.queryset.filter(status='pending')
        serializer = self.get_serializer(admissions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='approved')
    def approved(self, request):
        admissions = self.queryset.filter(status='approved')
        serializer = self.get_serializer(admissions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='convert-to-student')
    def convert_to_student(self, request, pk=None):
        admission = self.get_object()
        if admission.status != 'approved':
            return Response({"detail": "Admission must be approved before conversion."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ConvertToStudentSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                # 1. Create User
                username = f"stu{serializer.validated_data['admission_number']}"
                user = User.objects.create_user(
                    email=admission.email or f"{username}@school.local",
                    username=username,
                    password=username, # Default password
                    first_name=admission.first_name,
                    last_name=admission.last_name,
                    role='student'
                )
                
                # 2. Create StudentProfile
                student = StudentProfile.objects.create(
                    user=user,
                    admission_number=serializer.validated_data['admission_number'],
                    date_of_birth=admission.date_of_birth,
                    gender=admission.gender,
                    address=admission.address
                )
                
                # 3. Update admission status
                admission.status = 'converted'
                admission.save()
                
            return Response({"detail": "Successfully converted to student.", "student_id": student.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdmissionDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = AdmissionDocumentSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        return AdmissionDocument.objects.filter(admission_id=self.kwargs['admission_pk'])

    def perform_create(self, serializer):
        admission = get_object_or_404(Admission, pk=self.kwargs['admission_pk'])
        serializer.save(admission=admission)
