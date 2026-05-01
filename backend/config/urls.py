"""
URL configuration for nifty100 project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    
    path('api/companies/', include('apps.companies.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/screener/', include('apps.screener.urls')),
    path('api/ml/', include('apps.ml_engine.urls')),
    path('api/partner/', include('apps.partner_api.urls')),
    path('api/dashboards/', include('apps.dashboards.urls')),
    path('api/api-keys/', include('apps.api_keys.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
