from http.server import BaseHTTPRequestHandler
import os
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Ajouter le répertoire du projet au Python path
project_dir = Path(__file__).resolve().parent / 'pipou_blog'
sys.path.insert(0, str(project_dir))

# Configurer les variables d'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipou_blog.settings')

import django
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

# Initialiser Django
django.setup()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Test simple
            if self.path == '/test':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                db_status = 'SET' if os.getenv('DATABASE_URL') else 'NOT SET'
                response = f"Django OK! DATABASE_URL: {db_status}"
                self.wfile.write(response.encode())
                return
            
            # Pour toutes les autres routes, utiliser Django
            from django.core.handlers.wsgi import WSGIHandler
            from django.http import HttpRequest
            
            # Créer une requête Django
            request = HttpRequest()
            request.method = 'GET'
            request.path = self.path
            
            # Obtenir l'application Django
            django_app = get_wsgi_application()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Django app loaded successfully!")
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"Erreur: {str(e)}".encode())
    
    def do_POST(self):
        self.do_GET()
