from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DirectoryContact
from .serializers import DirectoryContactSerializer
from django.db.models import Q

class DirectoryContactViewSet(viewsets.ModelViewSet):
    queryset = DirectoryContact.objects.all()
    serializer_class = DirectoryContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"detail": "q parameter is required for search."}, status=status.HTTP_400_BAD_REQUEST)
        
        contacts = self.queryset.filter(
            Q(name__icontains=query) | 
            Q(role__icontains=query) | 
            Q(phone_number__icontains=query) | 
            Q(email__icontains=query)
        )
        serializer = self.get_serializer(contacts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-role')
    def by_role(self, request):
        role = request.query_params.get('role')
        if not role:
            return Response({"detail": "role parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        contacts = self.queryset.filter(role__icontains=role)
        serializer = self.get_serializer(contacts, many=True)
        return Response(serializer.data)
