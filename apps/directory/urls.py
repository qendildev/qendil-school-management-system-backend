from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DirectoryContactViewSet

router = DefaultRouter()
router.register(r'', DirectoryContactViewSet, basename='directory')

app_name = 'directory'

urlpatterns = [
    path('', include(router.urls)),
]
