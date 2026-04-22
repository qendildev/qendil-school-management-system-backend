from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Promotion
from .serializers import PromotionSerializer, BulkPromotionSerializer
from apps.students.models import StudentProfile
from apps.classes.models import Class, Section
from apps.settings_app.models import AcademicYear
from apps.core.permissions import IsAdminOrSuperAdmin

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    @action(detail=False, methods=['get'], url_path='history')
    def history(self, request):
        promotions = self.queryset.order_by('-created_at')
        serializer = self.get_serializer(promotions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='eligible-students')
    def eligible_students(self, request):
        # Placeholder for logic to find students eligible for promotion
        # e.g. those in a specific class/section who passed exams
        return Response({"detail": "Logic for eligible students pending."})

    @action(detail=False, methods=['post'], url_path='bulk-promote')
    def bulk_promote(self, request):
        serializer = BulkPromotionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            student_ids = data['student_ids']
            
            from_class = get_object_or_404(Class, pk=data['from_class_id'])
            from_section = get_object_or_404(Section, pk=data['from_section_id'])
            from_year = get_object_or_404(AcademicYear, pk=data['from_academic_year_id'])
            
            to_class = get_object_or_404(Class, pk=data['to_class_id'])
            to_section = get_object_or_404(Section, pk=data['to_section_id'])
            to_year = get_object_or_404(AcademicYear, pk=data['to_academic_year_id'])
            
            promotions_to_create = []
            
            with transaction.atomic():
                for s_id in student_ids:
                    student = get_object_or_404(StudentProfile, pk=s_id)
                    
                    promotion = Promotion(
                        student=student,
                        from_class=from_class,
                        from_section=from_section,
                        from_academic_year=from_year,
                        to_class=to_class,
                        to_section=to_section,
                        to_academic_year=to_year,
                        status=data.get('status', 'promoted'),
                        remarks=data.get('remarks', '')
                    )
                    promotions_to_create.append(promotion)
                    
                    # Update student's academic year on profile
                    student.academic_year = to_year
                    student.save()
                    
                Promotion.objects.bulk_create(promotions_to_create)
                
            return Response({"detail": f"Successfully promoted {len(promotions_to_create)} students."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='promote-students')
    def promote_students(self, request):
        # Alias for bulk_promote or single student promotion logic
        return self.bulk_promote(request)
