import os
from django.http import JsonResponse
from django.conf import settings

def debug_info(request):
    """Vue de debug pour diagnostiquer les problèmes de configuration"""
    
    debug_data = {
        'status': 'Django is running!',
        'python_version': os.sys.version,
        'django_version': getattr(settings, 'DJANGO_VERSION', 'Unknown'),
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
