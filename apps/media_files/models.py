from django.db import models
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class MediaAlbum(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='media_albums')

    def __str__(self):
        return self.title

class MediaFile(TimeStampedModel):
    album = models.ForeignKey(MediaAlbum, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_files')
    file_type = models.CharField(max_length=50, blank=True) # e.g. 'image/png', 'application/pdf'

    def __str__(self):
        return self.title or self.file.name
