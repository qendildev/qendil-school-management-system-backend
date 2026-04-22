from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import BookCategory, Book, BookIssue
from .serializers import (
    BookCategorySerializer, BookSerializer, 
    BookIssueSerializer, IssueBookSerializer
)
from apps.students.models import StudentProfile
from apps.core.permissions import IsAdminOrSuperAdmin, IsLibrarian

class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    permission_classes = [IsAdminOrSuperAdmin | IsLibrarian]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search', 'available']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrSuperAdmin | IsLibrarian]

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"detail": "q parameter is required for search."}, status=status.HTTP_400_BAD_REQUEST)
        
        books = self.queryset.filter(title__icontains=query) | self.queryset.filter(author__icontains=query)
        serializer = self.get_serializer(books.distinct(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        books = self.queryset.filter(available_quantity__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsAdminOrSuperAdmin | IsLibrarian]

    def create(self, request, *args, **kwargs):
        serializer = IssueBookSerializer(data=request.data)
        if serializer.is_valid():
            book = get_object_or_404(Book, pk=serializer.validated_data['book_id'])
            student = get_object_or_404(StudentProfile, pk=serializer.validated_data['student_id'])
            
            if not book.is_available:
                return Response({"detail": "Book is not available."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create issue
            issue = BookIssue.objects.create(
                book=book,
                student=student,
                due_date=serializer.validated_data['due_date']
            )
            
            # Update book quantity
            book.available_quantity -= 1
            book.save()
            
            response_serializer = self.get_serializer(issue)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='return')
    def return_book(self, request, pk=None):
        issue = self.get_object()
        if issue.status == 'returned':
            return Response({"detail": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST)
        
        issue.status = 'returned'
        issue.return_date = timezone.now().date()
        issue.save()
        
        # Increment available quantity
        book = issue.book
        if book.available_quantity < book.quantity:
            book.available_quantity += 1
            book.save()
            
        return Response({"detail": "Book returned successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue(self, request):
        today = timezone.now().date()
        issues = self.queryset.filter(status='issued', due_date__lt=today)
        serializer = self.get_serializer(issues, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'by-student/(?P<student_id>\d+)')
    def by_student(self, request, student_id=None):
        issues = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(issues, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='reports')
    def reports(self, request):
        return Response({"detail": "Library reports module pending integration."})
