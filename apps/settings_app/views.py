from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import SchoolInfo, AcademicYear, GeneralSettings, Role, Permission
from .serializers import (
    SchoolInfoSerializer, AcademicYearSerializer, GeneralSettingsSerializer,
    RoleSerializer, PermissionSerializer
)
from apps.core.permissions import IsSuperAdmin, IsAdminOrSuperAdmin

class SchoolInfoView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]

    def get(self, request):
        info = SchoolInfo.objects.first()
        if not info:
            info = SchoolInfo.objects.create(name="Qendil School")
        serializer = SchoolInfoSerializer(info)
        return Response(serializer.data)

    def put(self, request):
        info = SchoolInfo.objects.first()
        if not info:
            info = SchoolInfo.objects.create(name="Qendil School")
        serializer = SchoolInfoSerializer(info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GeneralSettingsView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]

    def get(self, request):
        settings = GeneralSettings.objects.first()
        if not settings:
            settings = GeneralSettings.objects.create()
        serializer = GeneralSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request):
        settings = GeneralSettings.objects.first()
        if not settings:
            settings = GeneralSettings.objects.create()
        serializer = GeneralSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcademicYearActiveView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]

    def get(self, request):
        active_year = AcademicYear.objects.filter(is_active=True).first()
        if active_year:
            serializer = AcademicYearSerializer(active_year)
            return Response(serializer.data)
        return Response({"detail": "No active academic year found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        year_id = request.data.get('academic_year_id')
        if not year_id:
            return Response({"detail": "academic_year_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        AcademicYear.objects.all().update(is_active=False)
        year = get_object_or_404(AcademicYear, id=year_id)
        year.is_active = True
        year.save()
        serializer = AcademicYearSerializer(year)
        return Response(serializer.data)

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAdminOrSuperAdmin]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsSuperAdmin]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsSuperAdmin]

class RolePermissionsView(APIView):
    permission_classes = [IsSuperAdmin]

    def put(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        permission_ids = request.data.get('permission_ids', [])
        permissions = Permission.objects.filter(id__in=permission_ids)
        role.permissions.set(permissions)
        serializer = RoleSerializer(role)
        return Response(serializer.data)
