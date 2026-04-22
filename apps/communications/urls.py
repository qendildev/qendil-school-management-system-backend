from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, CommunicationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'', CommunicationViewSet, basename='communication')

app_name = 'communications'

urlpatterns = [
    path('', include(router.urls)),
]
