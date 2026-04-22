from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Event, EventRSVP
from .serializers import EventSerializer, EventRSVPSerializer, RSVPActionSerializer
from apps.core.permissions import IsAdminOrSuperAdmin

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'upcoming', 'calendar', 'by_month', 'rsvp', 'attendees']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrSuperAdmin()]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        event = self.get_object()
        event.is_published = True
        event.save()
        return Response({"detail": "Event published."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        now = timezone.now()
        events = self.queryset.filter(is_published=True, start_date__gte=now).order_by('start_date')
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='calendar')
    def calendar(self, request):
        events = self.queryset.filter(is_published=True)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-month')
    def by_month(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year', timezone.now().year)
        
        if not month:
            return Response({"detail": "month parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        events = self.queryset.filter(is_published=True, start_date__month=month, start_date__year=year)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='rsvp')
    def rsvp(self, request, pk=None):
        event = self.get_object()
        serializer = RSVPActionSerializer(data=request.data)
        if serializer.is_valid():
            rsvp, created = EventRSVP.objects.get_or_create(
                event=event,
                user=request.user,
                defaults={'status': serializer.validated_data['status']}
            )
            if not created:
                rsvp.status = serializer.validated_data['status']
                rsvp.save()
            return Response({"detail": "RSVP updated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='attendees')
    def attendees(self, request, pk=None):
        event = self.get_object()
        rsvps = event.rsvps.all()
        serializer = EventRSVPSerializer(rsvps, many=True)
        return Response(serializer.data)
