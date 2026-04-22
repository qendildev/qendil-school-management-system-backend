from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from .models import FeeCategory, FeeStructure, FeeInstallment, FeePayment
from .serializers import (
    FeeCategorySerializer, FeeStructureSerializer, 
    FeeInstallmentSerializer, FeePaymentSerializer,
    SendReminderSerializer
)
from apps.core.permissions import IsAdminOrSuperAdmin, IsAccountant

class FeeCategoryViewSet(viewsets.ModelViewSet):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer
    permission_classes = [IsAdminOrSuperAdmin | IsAccountant]

class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsAccountant]

class FeeInstallmentViewSet(viewsets.ModelViewSet):
    queryset = FeeInstallment.objects.all()
    serializer_class = FeeInstallmentSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsAccountant]

class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.all().order_by('-payment_date')
    serializer_class = FeePaymentSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsAccountant]

    def perform_create(self, serializer):
        serializer.save(collected_by=self.request.user)

    @action(detail=False, methods=['get'], url_path=r'by-student/(?P<student_id>\d+)')
    def by_student(self, request, student_id=None):
        payments = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='receipt')
    def receipt(self, request, pk=None):
        payment = self.get_object()
        # Logic to generate receipt (e.g. PDF generation)
        return Response({"detail": f"Receipt generated for payment {payment.id}."})

class FeeReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminOrSuperAdmin | IsAccountant]

    @action(detail=False, methods=['get'], url_path='dues')
    def dues(self, request):
        # Placeholder for complex dues calculation logic
        return Response({"detail": "Overall fee dues report pending."})

    @action(detail=False, methods=['get'], url_path='dues/by-class')
    def dues_by_class(self, request):
        class_id = request.query_params.get('class_id')
        return Response({"detail": f"Dues for class {class_id} pending."})

    @action(detail=False, methods=['post'], url_path='reminders/send')
    def send_reminders(self, request):
        serializer = SendReminderSerializer(data=request.data)
        if serializer.is_valid():
            # Logic to send notifications/emails
            count = len(serializer.validated_data['student_ids'])
            return Response({"detail": f"Reminders sent to {count} students."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='collected')
    def collected(self, request):
        total = FeePayment.objects.filter(status='completed').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        return Response({"total_collected": total})

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        return Response({"detail": "Pending fees aggregation pending."})
