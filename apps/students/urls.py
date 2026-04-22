from django.urls import path, include
from rest_framework_nested import routers
from .views import StudentProfileViewSet, StudentDocumentViewSet

router = routers.DefaultRouter()
router.register(r'', StudentProfileViewSet, basename='student')

student_router = routers.NestedDefaultRouter(router, r'', lookup='student')
student_router.register(r'documents', StudentDocumentViewSet, basename='student-documents')

app_name = 'students'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(student_router.urls)),
]
