from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountCategoryViewSet, TransactionViewSet, ReportViewSet

router = DefaultRouter()
router.register(r'categories', AccountCategoryViewSet, basename='account-category')
router.register(r'reports', ReportViewSet, basename='account-reports')
router.register(r'transactions', TransactionViewSet, basename='transaction')

app_name = 'accounts'

urlpatterns = [
    # Custom routes to handle /api/accounts/income and /api/accounts/expenses without id
    path('income/', TransactionViewSet.as_view({'get': 'income', 'post': 'income'}), name='income-list'),
    path('expenses/', TransactionViewSet.as_view({'get': 'expenses', 'post': 'expenses'}), name='expense-list'),
    path('balance/', ReportViewSet.as_view({'get': 'balance'}), name='account-balance'),
    path('', include(router.urls)),
]
