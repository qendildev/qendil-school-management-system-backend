from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaAlbumViewSet, MediaFileViewSet

router = DefaultRouter()
router.register(r'albums', MediaAlbumViewSet, basename='media-album')
router.register(r'', MediaFileViewSet, basename='media-file')

app_name = 'media_files'

urlpatterns = [
    path('', include(router.urls)),
]
