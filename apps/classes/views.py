from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Class, Section, ClassTeacher
from apps.staff.models import StaffProfile
from apps.students.models import StudentProfile
from apps.students.serializers import StudentProfileSerializer
from .serializers import ClassSerializer, SectionSerializer, AssignTeacherSerializer
from apps.core.permissions import IsAdminOrSuperAdmin

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    @action(detail=True, methods=['post'], url_path='assign-teacher')
    def assign_teacher(self, request, pk=None):
        class_obj = self.get_object()
        serializer = AssignTeacherSerializer(data=request.data)
        if serializer.is_valid():
            section = get_object_or_404(Section, pk=serializer.validated_data['section_id'], class_name=class_obj)
            teacher = get_object_or_404(StaffProfile, pk=serializer.validated_data['teacher_id'])
            
            ct, created = ClassTeacher.objects.get_or_create(
                section=section,
                defaults={'teacher': teacher}
            )
            if not created:
                ct.teacher = teacher
                ct.save()
            return Response({"detail": "Teacher assigned to section successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='students')
    def students(self, request, pk=None):
        # We'd ideally join through a StudentClassLink, but for now we just filter on any student 
        # (This will be fleshed out when admission is fully mapped). 
        # For now, let's return a placeholder or empty list.
        return Response({"detail": "Student listing for class will be implemented."})

    @action(detail=True, methods=['get'], url_path='subjects')
    def subjects(self, request, pk=None):
        return Response({"detail": "Subjects module integration pending."})

    @action(detail=True, methods=['get'], url_path='timetable')
    def timetable(self, request, pk=None):
        return Response({"detail": "Timetable module integration pending."})

class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        return Section.objects.filter(class_name_id=self.kwargs['class_pk'])

    def perform_create(self, serializer):
        class_obj = get_object_or_404(Class, pk=self.kwargs['class_pk'])
        serializer.save(class_name=class_obj)
