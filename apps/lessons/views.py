from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Lesson, Timetable
from .serializers import LessonSerializer, TimetableSerializer
from apps.core.permissions import IsAdminOrSuperAdmin, IsTeacher

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsTeacher]

    @action(detail=False, methods=['get'], url_path=r'by-class/(?P<class_id>\d+)')
    def by_class(self, request, class_id=None):
        lessons = self.queryset.filter(class_name_id=class_id)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'by-subject/(?P<subject_id>\d+)')
    def by_subject(self, request, subject_id=None):
        lessons = self.queryset.filter(subject_id=subject_id)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    @action(detail=False, methods=['get'], url_path=r'by-class/(?P<class_id>\d+)')
    def by_class(self, request, class_id=None):
        timetables = self.queryset.filter(class_name_id=class_id)
        serializer = self.get_serializer(timetables, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'by-teacher/(?P<teacher_id>\d+)')
    def by_teacher(self, request, teacher_id=None):
        timetables = self.queryset.filter(teacher_id=teacher_id)
        serializer = self.get_serializer(timetables, many=True)
        return Response(serializer.data)
