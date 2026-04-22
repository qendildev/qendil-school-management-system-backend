from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SchoolInfoView, AcademicYearActiveView, AcademicYearViewSet, GeneralSettingsView,
    PermissionViewSet, RoleViewSet, RolePermissionsView
)

router = DefaultRouter()
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)

app_name = 'settings_app'

urlpatterns = [
    path('school-info/', SchoolInfoView.as_view(), name='school_info'),
    path('academic-year/', AcademicYearActiveView.as_view(), name='active_academic_year'),
    path('general/', GeneralSettingsView.as_view(), name='general_settings'),
    path('roles/<int:pk>/permissions/', RolePermissionsView.as_view(), name='role_permissions'),
    path('', include(router.urls)),
]
