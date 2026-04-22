from django.urls import path, include
from rest_framework_nested import routers
from .views import ClassViewSet, SectionViewSet

router = routers.DefaultRouter()
router.register(r'', ClassViewSet, basename='class')

class_router = routers.NestedDefaultRouter(router, r'', lookup='class')
class_router.register(r'sections', SectionViewSet, basename='class-sections')

app_name = 'classes'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(class_router.urls)),
]
