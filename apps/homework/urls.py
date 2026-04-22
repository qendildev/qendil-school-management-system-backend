from django.urls import path, include
from rest_framework_nested import routers
from .views import HomeworkViewSet, HomeworkSubmissionViewSet

router = routers.DefaultRouter()
router.register(r'', HomeworkViewSet, basename='homework')

homework_router = routers.NestedDefaultRouter(router, r'', lookup='homework')
homework_router.register(r'submissions', HomeworkSubmissionViewSet, basename='homework-submissions')

app_name = 'homework'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(homework_router.urls)),
]
