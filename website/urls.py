from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from pathlib import Path
from django.conf.urls.static import static

urlpatterns = [
    # your app urls
    path("admin/", admin.site.urls),
    path("reports/", include("reporting.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
