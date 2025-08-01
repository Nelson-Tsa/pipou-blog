"""
URL configuration for pipou_blog project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import os

from django.conf import settings
from django.conf.urls.static import static

def simple_test(request):
    """Vue de test ultra-simple"""
    try:
        return HttpResponse(f"Django OK! DATABASE_URL: {'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")
    except Exception as e:
        return HttpResponse(f"Erreur: {str(e)}")

urlpatterns = [
    path('test/', simple_test, name='test'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('profile/', include('user_profile.urls')),
    path('', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
