from django.urls import path, include
from rest_framework_nested import routers
from .views import AdmissionViewSet, AdmissionDocumentViewSet

router = routers.DefaultRouter()
router.register(r'', AdmissionViewSet, basename='admission')

admission_router = routers.NestedDefaultRouter(router, r'', lookup='admission')
admission_router.register(r'documents', AdmissionDocumentViewSet, basename='admission-documents')

app_name = 'admissions'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(admission_router.urls)),
]
