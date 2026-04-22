from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Subject, SubjectTeacher, Curriculum
from apps.staff.models import StaffProfile
from apps.classes.models import Class
from .serializers import (
    SubjectSerializer, SubjectTeacherSerializer, CurriculumSerializer, AssignTeacherToSubjectSerializer
)
from apps.core.permissions import IsAdminOrSuperAdmin

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    @action(detail=True, methods=['post'], url_path='assign-teacher')
    def assign_teacher(self, request, pk=None):
        subject = self.get_object()
        serializer = AssignTeacherToSubjectSerializer(data=request.data)
        if serializer.is_valid():
            teacher = get_object_or_404(StaffProfile, pk=serializer.validated_data['teacher_id'])
            assigned_class = get_object_or_404(Class, pk=serializer.validated_data['assigned_class_id'])
            
            st, created = SubjectTeacher.objects.get_or_create(
                subject=subject,
                assigned_class=assigned_class,
                defaults={'teacher': teacher}
            )
            if not created:
                st.teacher = teacher
                st.save()
            return Response({"detail": "Teacher assigned to subject successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='classes')
    def classes(self, request, pk=None):
        subject = self.get_object()
        subject_teachers = SubjectTeacher.objects.filter(subject=subject)
        classes = [st.assigned_class for st in subject_teachers]
        # remove duplicates
        classes = list(set(classes))
        from apps.classes.serializers import ClassSerializer
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)

class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    permission_classes = [IsAdminOrSuperAdmin]
