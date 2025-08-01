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
    return HttpResponse("Django fonctionne ! Variables: DATABASE_URL=" + 
                       ("SET" if os.getenv('DATABASE_URL') else "NOT SET"))

def debug_info(request):
    """Vue de debug pour diagnostiquer les problèmes de configuration"""
    try:
        debug_data = {
            'status': 'Django is running!',
            'environment_variables': {
                'DATABASE_URL': 'SET' if os.getenv('DATABASE_URL') else 'NOT SET',
                'SECRET_KEY': 'SET' if os.getenv('SECRET_KEY') else 'NOT SET',
                'DEBUG': os.getenv('DEBUG', 'NOT SET'),
            }
        }
        
        from django.http import JsonResponse
        return JsonResponse(debug_data, indent=2)
    except Exception as e:
        return HttpResponse(f"Erreur debug: {str(e)}")

urlpatterns = [
    path('test/', simple_test, name='test'),  # Vue de test simple
    path('debug/', debug_info, name='debug'),  # Vue de debug
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('profile/', include('user_profile.urls')),
    path('', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
