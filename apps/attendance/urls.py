from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentAttendanceViewSet, StaffAttendanceViewSet

router = DefaultRouter()
router.register(r'students', StudentAttendanceViewSet, basename='student-attendance')
router.register(r'staff', StaffAttendanceViewSet, basename='staff-attendance')

app_name = 'attendance'

urlpatterns = [
    path('', include(router.urls)),
]
