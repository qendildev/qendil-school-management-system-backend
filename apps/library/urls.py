from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookCategoryViewSet, BookViewSet, BookIssueViewSet

router = DefaultRouter()
router.register(r'categories', BookCategoryViewSet, basename='book-category')
router.register(r'issues', BookIssueViewSet, basename='book-issue')
router.register(r'books', BookViewSet, basename='book')

app_name = 'library'

urlpatterns = [
    path('', include(router.urls)),
]
