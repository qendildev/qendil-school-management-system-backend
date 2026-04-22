from rest_framework import views, status, permissions
from rest_framework.response import Response
from apps.core.permissions import IsAdminOrSuperAdmin, IsTeacher, IsStudent, IsParent, IsAccountant
from apps.students.models import StudentProfile
from apps.staff.models import StaffProfile
from apps.classes.models import Class
from apps.accounts.models import Transaction
from django.db.models import Sum

class AdminDashboardView(views.APIView):
    permission_classes = [IsAdminOrSuperAdmin]

    def get(self, request):
        total_students = StudentProfile.objects.filter(is_deleted=False).count()
        total_staff = StaffProfile.objects.filter(is_deleted=False).count()
        total_classes = Class.objects.count()
        
        income = Transaction.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        balance = income - expense

        return Response({
            "total_students": total_students,
            "total_staff": total_staff,
            "total_classes": total_classes,
            "financials": {
                "income": income,
                "expense": expense,
                "balance": balance
            }
        })

class TeacherDashboardView(views.APIView):
    permission_classes = [IsTeacher | IsAdminOrSuperAdmin]

    def get(self, request):
        # Specific teacher data
        return Response({
            "assigned_classes": 0, # Placeholder
            "pending_homeworks_to_grade": 0, # Placeholder
            "today_lessons": 0 # Placeholder
        })

class StudentDashboardView(views.APIView):
    permission_classes = [IsStudent | IsAdminOrSuperAdmin]

    def get(self, request):
        return Response({
            "attendance_percentage": 0, # Placeholder
            "pending_homeworks": 0, # Placeholder
            "upcoming_exams": 0 # Placeholder
        })

class ParentDashboardView(views.APIView):
    permission_classes = [IsParent | IsAdminOrSuperAdmin]

    def get(self, request):
        return Response({
            "children_count": 0, # Placeholder
            "fee_dues": 0, # Placeholder
            "unread_notifications": 0 # Placeholder
        })

class AccountantDashboardView(views.APIView):
    permission_classes = [IsAccountant | IsAdminOrSuperAdmin]

    def get(self, request):
        income = Transaction.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            "total_income": income,
            "total_expense": expense,
            "pending_fee_payments": 0, # Placeholder
            "recent_transactions": [] # Placeholder
        })

# Global Reports API endpoints as requested
class ReportsView(views.APIView):
    permission_classes = [IsAdminOrSuperAdmin]

    def get(self, request, report_type):
        if report_type == 'students':
            return Response({"detail": "Students report placeholder."})
        elif report_type == 'attendance':
            return Response({"detail": "Attendance report placeholder."})
        elif report_type == 'academic':
            return Response({"detail": "Academic report placeholder."})
        elif report_type == 'financial':
            return Response({"detail": "Financial report placeholder."})
        elif report_type == 'staff':
            return Response({"detail": "Staff report placeholder."})
        else:
            return Response({"detail": "Invalid report type."}, status=status.HTTP_400_BAD_REQUEST)
