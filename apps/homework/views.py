from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Homework, HomeworkSubmission
from .serializers import HomeworkSerializer, HomeworkSubmissionSerializer, GradeSubmissionSerializer
from apps.core.permissions import IsAdminOrSuperAdmin, IsTeacher

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsTeacher]

    @action(detail=False, methods=['get'], url_path=r'by-class/(?P<class_id>\d+)')
    def by_class(self, request, class_id=None):
        homeworks = self.queryset.filter(class_name_id=class_id)
        serializer = self.get_serializer(homeworks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'by-subject/(?P<subject_id>\d+)')
    def by_subject(self, request, subject_id=None):
        homeworks = self.queryset.filter(subject_id=subject_id)
        serializer = self.get_serializer(homeworks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'student/(?P<student_id>\d+)')
    def by_student(self, request, student_id=None):
        # Find homeworks via submissions or class logic
        submissions = HomeworkSubmission.objects.filter(student_id=student_id)
        homeworks = [sub.homework for sub in submissions]
        serializer = self.get_serializer(homeworks, many=True)
        return Response(serializer.data)

class HomeworkSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsTeacher]

    def get_queryset(self):
        return HomeworkSubmission.objects.filter(homework_id=self.kwargs['homework_pk'])

    def perform_create(self, serializer):
        homework = get_object_or_404(Homework, pk=self.kwargs['homework_pk'])
        serializer.save(homework=homework)

    @action(detail=True, methods=['post'], url_path='grade')
    def grade(self, request, homework_pk=None, pk=None):
        submission = self.get_object()
        serializer = GradeSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission.marks_obtained = serializer.validated_data['marks_obtained']
            submission.remarks = serializer.validated_data.get('remarks', submission.remarks)
            submission.status = 'graded'
            submission.save()
            return Response({"detail": "Submission graded successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
