import os
import sys
import traceback
from pathlib import Path

def handler(request, response):
    try:
        # Ajouter le répertoire du projet au Python path
        project_dir = Path(__file__).resolve().parent / 'pipou_blog'
        sys.path.insert(0, str(project_dir))

        # Configurer les variables d'environnement Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipou_blog.settings')

        # Test des variables d'environnement
        debug_info = []
        debug_info.append(f"DATABASE_URL: {'✅ SET' if os.environ.get('DATABASE_URL') else '❌ MISSING'}")
        debug_info.append(f"SECRET_KEY: {'✅ SET' if os.environ.get('SECRET_KEY') else '❌ MISSING'}")
        debug_info.append(f"DEBUG: {os.environ.get('DEBUG', 'NOT SET')}")
        
        # Tenter d'initialiser Django
        try:
            import django
            debug_info.append("✅ Django import OK")
            
            django.setup()
            debug_info.append("✅ Django setup OK")
            
            from django.core.wsgi import get_wsgi_application
            debug_info.append("✅ WSGI import OK")
            
            app = get_wsgi_application()
            debug_info.append("✅ WSGI app created OK")
            
            # Si tout va bien, retourner l'app Django
            return app
            
        except Exception as django_error:
            debug_info.append(f"❌ Django Error: {str(django_error)}")
            debug_info.append(f"❌ Traceback: {traceback.format_exc()}")
        
        # Retourner une page de diagnostic
        debug_html = f"""
        <html>
        <head><title>Django Debug - Vercel</title></head>
        <body>
            <h1>🔍 Django Diagnostic</h1>
            <h2>Environment Check:</h2>
            <ul>
                {''.join([f'<li>{info}</li>' for info in debug_info])}
            </ul>
            <h2>Python Path:</h2>
            <ul>
                {''.join([f'<li>{path}</li>' for path in sys.path[:5]])}
            </ul>
        </body>
        </html>
        """
        
        def simple_app(environ, start_response):
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [debug_html.encode('utf-8')]
        
        return simple_app
        
    except Exception as e:
        # Erreur critique - retourner une page d'erreur simple
        error_html = f"""
        <html>
        <head><title>Critical Error</title></head>
        <body>
            <h1>❌ Critical Error</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <pre>{traceback.format_exc()}</pre>
        </body>
        </html>
        """
        
        def error_app(environ, start_response):
            start_response('500 Internal Server Error', [('Content-Type', 'text/html')])
            return [error_html.encode('utf-8')]
        
        return error_app
