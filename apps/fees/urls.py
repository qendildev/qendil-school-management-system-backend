from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeeCategoryViewSet, FeeStructureViewSet, 
    FeeInstallmentViewSet, FeePaymentViewSet,
    FeeReportViewSet
)

router = DefaultRouter()
router.register(r'categories', FeeCategoryViewSet, basename='fee-category')
router.register(r'structures', FeeStructureViewSet, basename='fee-structure')
router.register(r'installments', FeeInstallmentViewSet, basename='fee-installment')
router.register(r'payments', FeePaymentViewSet, basename='fee-payment')

app_name = 'fees'

urlpatterns = [
    # Custom routes mapping to FeeReportViewSet methods
    path('dues/', FeeReportViewSet.as_view({'get': 'dues'}), name='fee-dues'),
    path('dues/by-class/', FeeReportViewSet.as_view({'get': 'dues_by_class'}), name='fee-dues-by-class'),
    path('reminders/send/', FeeReportViewSet.as_view({'post': 'send_reminders'}), name='fee-reminders-send'),
    path('reports/collected/', FeeReportViewSet.as_view({'get': 'collected'}), name='fee-reports-collected'),
    path('reports/pending/', FeeReportViewSet.as_view({'get': 'pending'}), name='fee-reports-pending'),
    
    path('', include(router.urls)),
]
