from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import ParentProfile, ParentStudentLink
from apps.students.models import StudentProfile
from .serializers import ParentProfileSerializer, ParentStudentLinkSerializer, LinkStudentSerializer
from apps.core.permissions import IsAdminOrSuperAdmin

class ParentProfileViewSet(viewsets.ModelViewSet):
    queryset = ParentProfile.objects.filter(is_deleted=False)
    serializer_class = ParentProfileSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete() # uses soft delete
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='children')
    def children(self, request, pk=None):
        parent = self.get_object()
        links = ParentStudentLink.objects.filter(parent=parent)
        serializer = ParentStudentLinkSerializer(links, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='link-student')
    def link_student(self, request, pk=None):
        parent = self.get_object()
        serializer = LinkStudentSerializer(data=request.data)
        if serializer.is_valid():
            student = get_object_or_404(StudentProfile, pk=serializer.validated_data['student_id'])
            link, created = ParentStudentLink.objects.get_or_create(
                parent=parent,
                student=student,
                defaults={'relationship': serializer.validated_data['relationship']}
            )
            if not created:
                link.relationship = serializer.validated_data['relationship']
                link.save()
            return Response({"detail": "Student linked successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path=r'unlink-student/(?P<student_id>\d+)')
    def unlink_student(self, request, pk=None, student_id=None):
        parent = self.get_object()
        link = get_object_or_404(ParentStudentLink, parent=parent, student_id=student_id)
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='notifications')
    def notifications(self, request, pk=None):
        return Response({"detail": "Communications module integration pending."})
