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

def test_template(request):
    """Test template simple sans base de données"""
    from django.shortcuts import render
    try:
        context = {
            'posts': [],  # Liste vide pour éviter l'erreur de base de données
            'user': request.user,
            'test_message': 'Template fonctionne ! 🎉'
        }
        return render(request, 'index_simple.html', context)
    except Exception as e:
        return HttpResponse(f"Erreur template: {str(e)}")

def run_migrations(request):
    """Exécuter les migrations Django via le web"""
    try:
        from django.core.management import execute_from_command_line
        import io
        import sys
        
        # Capturer la sortie
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            execute_from_command_line(['manage.py', 'migrate'])
            output = captured_output.getvalue()
            return HttpResponse(f"✅ Migrations exécutées avec succès!\n\n{output}")
        finally:
            sys.stdout = old_stdout
            
    except Exception as e:
        return HttpResponse(f"❌ Erreur lors des migrations: {str(e)}")

urlpatterns = [
    path('test/', simple_test, name='test'),
    path('test-template/', test_template, name='test_template'),
    path('migrate/', run_migrations, name='migrate'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('profile/', include('user_profile.urls')),
    path('', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
