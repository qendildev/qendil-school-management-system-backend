from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import ClassPost, PostComment, PostLike
from .serializers import ClassPostSerializer, PostCommentSerializer
from apps.classes.models import Class

class ClassPostViewSet(viewsets.ModelViewSet):
    queryset = ClassPost.objects.all().order_by('-is_pinned', '-created_at')
    serializer_class = ClassPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if 'class_pk' in self.kwargs:
            return self.queryset.filter(class_name_id=self.kwargs['class_pk'])
        return self.queryset

    def perform_create(self, serializer):
        class_obj = get_object_or_404(Class, pk=self.kwargs['class_pk'])
        serializer.save(author=self.request.user, class_name=class_obj)

    @action(detail=True, methods=['post', 'delete'], url_path='like')
    def like(self, request, class_pk=None, pk=None):
        post = self.get_object()
        if request.method == 'POST':
            PostLike.objects.get_or_create(post=post, user=request.user)
            return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)
        else:
            PostLike.objects.filter(post=post, user=request.user).delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='pin')
    def pin(self, request, class_pk=None, pk=None):
        if not request.user.role in ['admin', 'superadmin', 'teacher']:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        post = self.get_object()
        # Unpin others in the same class if needed (optional logic)
        # ClassPost.objects.filter(class_name=post.class_name).update(is_pinned=False)
        post.is_pinned = True
        post.save()
        return Response({"detail": "Post pinned."}, status=status.HTTP_200_OK)

class PostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PostComment.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        post = get_object_or_404(ClassPost, pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)
