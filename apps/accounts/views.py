from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from django.utils import timezone
from .models import AccountCategory, Transaction
from .serializers import AccountCategorySerializer, TransactionSerializer
from apps.core.permissions import IsAdminOrSuperAdmin, IsAccountant

class AccountCategoryViewSet(viewsets.ModelViewSet):
    queryset = AccountCategory.objects.all()
    serializer_class = AccountCategorySerializer
    permission_classes = [IsAdminOrSuperAdmin | IsAccountant]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-date', '-created_at')
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsAccountant]

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

    @action(detail=False, methods=['get', 'post'], url_path='income')
    def income(self, request):
        if request.method == 'POST':
            # Create income logic
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Force type to income
                serializer.validated_data['type'] = 'income'
                serializer.save(recorded_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # GET
        incomes = self.queryset.filter(type='income')
        serializer = self.get_serializer(incomes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get', 'post'], url_path='expenses')
    def expenses(self, request):
        if request.method == 'POST':
            # Create expense logic
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Force type to expense
                serializer.validated_data['type'] = 'expense'
                serializer.save(recorded_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # GET
        expenses = self.queryset.filter(type='expense')
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)

class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminOrSuperAdmin | IsAccountant]

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        income = Transaction.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        balance = income - expense
        
        return Response({
            "total_income": income,
            "total_expense": expense,
            "balance": balance
        })

    @action(detail=False, methods=['get'], url_path='monthly')
    def monthly(self, request):
        month = request.query_params.get('month', timezone.now().month)
        year = request.query_params.get('year', timezone.now().year)
        
        income = Transaction.objects.filter(type='income', date__month=month, date__year=year).aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(type='expense', date__month=month, date__year=year).aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            "month": month,
            "year": year,
            "income": income,
            "expense": expense,
            "balance": income - expense
        })

    @action(detail=False, methods=['get'], url_path='annual')
    def annual(self, request):
        year = request.query_params.get('year', timezone.now().year)
        
        income = Transaction.objects.filter(type='income', date__year=year).aggregate(total=Sum('amount'))['total'] or 0
        expense = Transaction.objects.filter(type='expense', date__year=year).aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            "year": year,
            "income": income,
            "expense": expense,
            "balance": income - expense
        })

    @action(detail=False, methods=['get'], url_path='balance')
    def balance(self, request):
        # Alias for summary or specific account balance logic
        return self.summary(request)
