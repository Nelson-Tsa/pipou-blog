"""
URL configuration for pipou_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
import os

from django.conf import settings
from django.conf.urls.static import static

def debug_info(request):
    """Vue de debug pour diagnostiquer les problèmes de configuration"""
    
    debug_data = {
        'status': 'Django is running!',
        'python_version': os.sys.version,
        'debug_mode': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'environment_variables': {
            'DATABASE_URL': 'SET' if os.getenv('DATABASE_URL') else 'NOT SET',
            'SECRET_KEY': 'SET' if os.getenv('SECRET_KEY') else 'NOT SET',
            'DEBUG': os.getenv('DEBUG', 'NOT SET'),
        },
        'database_config': {
            'engine': settings.DATABASES['default']['ENGINE'],
            'name': settings.DATABASES['default']['NAME'],
            'host': settings.DATABASES['default']['HOST'],
            'port': settings.DATABASES['default']['PORT'],
        },
        'static_settings': {
            'static_url': settings.STATIC_URL,
            'static_root': getattr(settings, 'STATIC_ROOT', 'Not set'),
        }
    }
    
    return JsonResponse(debug_data, indent=2)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('debug/', debug_info, name='debug'),  # Vue de debug temporaire
    path('', include('blog.urls')),
    path('profile/', include('user_profile.urls')),
    path('', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
