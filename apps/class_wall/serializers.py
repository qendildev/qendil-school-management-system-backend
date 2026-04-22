from rest_framework import serializers
from .models import ClassPost, PostComment, PostLike
from apps.authentication.serializers import UserSerializer

class PostCommentSerializer(serializers.ModelSerializer):
    author_details = UserSerializer(source='author', read_only=True)

    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ('author', 'post')

class ClassPostSerializer(serializers.ModelSerializer):
    author_details = UserSerializer(source='author', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = ClassPost
        fields = '__all__'
        read_only_fields = ('author', 'class_name', 'is_pinned')

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False
