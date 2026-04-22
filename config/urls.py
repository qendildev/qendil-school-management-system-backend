from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API Endpoints
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/settings/', include('apps.settings_app.urls')),
    path('api/v1/staff/', include('apps.staff.urls')),
    path('api/v1/students/', include('apps.students.urls')),
    path('api/v1/parents/', include('apps.parents.urls')),
    path('api/v1/classes/', include('apps.classes.urls')),
    path('api/v1/subjects/', include('apps.subjects.urls')),
    path('api/v1/attendance/', include('apps.attendance.urls')),
    path('api/v1/homework/', include('apps.homework.urls')),
    path('api/v1/lessons/', include('apps.lessons.urls')),
    path('api/v1/admissions/', include('apps.admissions.urls')),
    path('api/v1/promotions/', include('apps.promotions.urls')),
    path('api/v1/leaves/', include('apps.leaves.urls')),
    path('api/v1/holidays/', include('apps.holidays.urls')),
    path('api/v1/communications/', include('apps.communications.urls')),
    path('api/v1/notices/', include('apps.notices.urls')),
    path('api/v1/events/', include('apps.events.urls')),
    path('api/v1/class-wall/', include('apps.class_wall.urls')),
    path('api/v1/library/', include('apps.library.urls')),
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
    path('api/v1/media/', include('apps.media_files.urls')),
    path('api/v1/discipline/', include('apps.discipline.urls')),
    path('api/v1/directory/', include('apps.directory.urls')),
    path('api/v1/tasks/', include('apps.tasks.urls')),
    path('api/v1/activity-log/', include('apps.activity_log.urls')),
    path('api/v1/fees/', include('apps.fees.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
