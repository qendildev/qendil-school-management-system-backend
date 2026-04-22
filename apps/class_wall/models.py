from django.db import models
from apps.core.models import TimeStampedModel
from apps.classes.models import Class
from django.contrib.auth import get_user_model

User = get_user_model()

class ClassPost(TimeStampedModel):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_posts')
    content = models.TextField()
    image = models.ImageField(upload_to='class_posts/', null=True, blank=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return f"Post by {self.author} in {self.class_name}"

class PostComment(TimeStampedModel):
    post = models.ForeignKey(ClassPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

class PostLike(TimeStampedModel):
    post = models.ForeignKey(ClassPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user} liked {self.post}"
