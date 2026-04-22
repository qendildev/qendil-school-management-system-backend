from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, TimetableViewSet

router = DefaultRouter()
router.register(r'timetable', TimetableViewSet, basename='timetable')
router.register(r'', LessonViewSet, basename='lesson')

app_name = 'lessons'

urlpatterns = [
    path('', include(router.urls)),
]
