from rest_framework import serializers
from .models import MediaAlbum, MediaFile
from apps.authentication.serializers import UserSerializer

class MediaFileSerializer(serializers.ModelSerializer):
    uploaded_by_details = UserSerializer(source='uploaded_by', read_only=True)

    class Meta:
        model = MediaFile
        fields = '__all__'
        read_only_fields = ('uploaded_by', 'file_type')

class MediaAlbumSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    files_count = serializers.IntegerField(source='files.count', read_only=True)

    class Meta:
        model = MediaAlbum
        fields = '__all__'
        read_only_fields = ('created_by',)

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    album_id = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.CharField(max_length=255, required=False, allow_blank=True)
