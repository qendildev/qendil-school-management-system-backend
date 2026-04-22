from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import MediaAlbum, MediaFile
from .serializers import MediaAlbumSerializer, MediaFileSerializer, FileUploadSerializer
from apps.core.permissions import IsAdminOrSuperAdmin

class MediaAlbumViewSet(viewsets.ModelViewSet):
    queryset = MediaAlbum.objects.all()
    serializer_class = MediaAlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'], url_path='files')
    def get_files(self, request, pk=None):
        album = self.get_object()
        files = album.files.all()
        serializer = MediaFileSerializer(files, many=True)
        return Response(serializer.data)

class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminOrSuperAdmin()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request):
        if not request.user.role in ['admin', 'superadmin', 'teacher']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            album = None
            if data.get('album_id'):
                album = get_object_or_404(MediaAlbum, pk=data['album_id'])
            
            uploaded_file = data['file']
            file_type = uploaded_file.content_type
            
            media_file = MediaFile.objects.create(
                album=album,
                title=data.get('title', ''),
                file=uploaded_file,
                uploaded_by=request.user,
                file_type=file_type
            )
            
            return Response(MediaFileSerializer(media_file).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
