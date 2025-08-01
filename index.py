from http.server import BaseHTTPRequestHandler
import os
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import io

# Ajouter le répertoire du projet au Python path
project_dir = Path(__file__).resolve().parent / 'pipou_blog'
sys.path.insert(0, str(project_dir))

# Configurer les variables d'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipou_blog.settings')

import django
from django.core.wsgi import get_wsgi_application
from django.test import RequestFactory

# Initialiser Django
django.setup()

# Obtenir l'application Django
django_app = get_wsgi_application()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Créer un environnement WSGI simulé
            environ = {
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': self.path,
                'QUERY_STRING': '',
                'CONTENT_TYPE': '',
                'CONTENT_LENGTH': '',
                'SERVER_NAME': 'localhost',
                'SERVER_PORT': '80',
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'https',
                'wsgi.input': io.StringIO(),
                'wsgi.errors': sys.stderr,
                'wsgi.multithread': False,
                'wsgi.multiprocess': True,
                'wsgi.run_once': False,
            }
            
            # Variables pour capturer la réponse
            response_data = []
            status = None
            headers = []
            
            def start_response(status_code, response_headers):
                nonlocal status, headers
                status = status_code
                headers = response_headers
            
            # Appeler l'application Django
            response = django_app(environ, start_response)
            
            # Envoyer la réponse
            status_code = int(status.split(' ')[0])
            self.send_response(status_code)
            
            for header_name, header_value in headers:
                self.send_header(header_name, header_value)
            self.end_headers()
            
            # Écrire le contenu de la réponse
            for data in response:
                if isinstance(data, str):
                    self.wfile.write(data.encode('utf-8'))
                else:
                    self.wfile.write(data)
                    
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_msg = f"""
            <h1>Erreur Django</h1>
            <p>Erreur: {str(e)}</p>
            <p>Path: {self.path}</p>
            <p>Django est chargé mais il y a une erreur dans le routage.</p>
            """
            self.wfile.write(error_msg.encode())
    
    def do_POST(self):
        # Pour les requêtes POST, on peut adapter la méthode
        self.do_GET()
