from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisciplineTypeViewSet, DisciplineRecordViewSet

router = DefaultRouter()
router.register(r'types', DisciplineTypeViewSet, basename='discipline-type')
router.register(r'', DisciplineRecordViewSet, basename='discipline-record')

app_name = 'discipline'

urlpatterns = [
    path('', include(router.urls)),
]
