from django.urls import path, include
from rest_framework_nested import routers
from .views import ClassPostViewSet, PostCommentViewSet
from apps.classes.views import ClassViewSet

router = routers.DefaultRouter()
router.register(r'classes', ClassViewSet, basename='class-list') # We need a base for nesting

# We want /api/class-wall/{class_id}/posts/
class_router = routers.NestedDefaultRouter(router, r'classes', lookup='class')
class_router.register(r'posts', ClassPostViewSet, basename='class-posts')

# We want /api/class-wall/posts/{post_id}/comments/
# And /api/class-wall/posts/{post_id}/like/
post_router = routers.DefaultRouter()
post_router.register(r'posts', ClassPostViewSet, basename='post-detail')

comment_router = routers.NestedDefaultRouter(post_router, r'posts', lookup='post')
comment_router.register(r'comments', PostCommentViewSet, basename='post-comments')

app_name = 'class_wall'

urlpatterns = [
    # Match /api/class-wall/{class_id}/posts/
    path('<int:class_pk>/posts/', ClassPostViewSet.as_view({'get': 'list', 'post': 'create'}), name='class-posts-list'),
    path('<int:class_pk>/posts/<int:pk>/pin/', ClassPostViewSet.as_view({'post': 'pin'}), name='class-posts-pin'),
    
    # Match /api/class-wall/posts/{id}/
    path('', include(post_router.urls)),
    path('', include(comment_router.urls)),
]
