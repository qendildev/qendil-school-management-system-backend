from rest_framework import serializers
from .models import BookCategory, Book, BookIssue
from apps.students.serializers import StudentProfileSerializer

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category_details = BookCategorySerializer(source='category', read_only=True)
    is_available = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = '__all__'

class BookIssueSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)
    student_details = StudentProfileSerializer(source='student', read_only=True)

    class Meta:
        model = BookIssue
        fields = '__all__'

class IssueBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)
    student_id = serializers.IntegerField(required=True)
    due_date = serializers.DateField(required=True)
