from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveTypeViewSet, LeaveApplicationViewSet

router = DefaultRouter()
router.register(r'types', LeaveTypeViewSet, basename='leave-type')
router.register(r'', LeaveApplicationViewSet, basename='leave-application')

app_name = 'leaves'

urlpatterns = [
    path('', include(router.urls)),
]
