from django.urls import path, include
from rest_framework_nested import routers
from .views import DepartmentViewSet, StaffProfileViewSet, StaffPayrollViewSet

router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'', StaffProfileViewSet, basename='staff')

staff_router = routers.NestedDefaultRouter(router, r'', lookup='staff')
staff_router.register(r'payroll', StaffPayrollViewSet, basename='staff-payroll')

app_name = 'staff'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(staff_router.urls)),
]
