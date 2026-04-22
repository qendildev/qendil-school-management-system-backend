from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Holiday
from .serializers import HolidaySerializer
from apps.core.permissions import IsAdminOrSuperAdmin

class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'upcoming', 'calendar', 'by_month']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrSuperAdmin()]

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        today = timezone.now().date()
        holidays = self.queryset.filter(start_date__gte=today).order_by('start_date')
        serializer = self.get_serializer(holidays, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='calendar')
    def calendar(self, request):
        # Can be filtered by year/month if needed
        holidays = self.queryset.all()
        serializer = self.get_serializer(holidays, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-month')
    def by_month(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year', timezone.now().year)
        
        if not month:
            return Response({"detail": "month parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        holidays = self.queryset.filter(start_date__month=month, start_date__year=year)
        serializer = self.get_serializer(holidays, many=True)
        return Response(serializer.data)
