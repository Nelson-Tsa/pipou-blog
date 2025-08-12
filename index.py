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

# Obtenir l'application WSGI
application = get_wsgi_application()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        return self.handle_request()
    
    def do_POST(self):
        return self.handle_request()
    
    def do_PUT(self):
        return self.handle_request()
    
    def do_DELETE(self):
        return self.handle_request()
    
    def do_PATCH(self):
        return self.handle_request()
    
    def handle_request(self):
        try:
            # Créer un objet environ pour WSGI
            environ = {
                'REQUEST_METHOD': self.command,
                'SCRIPT_NAME': '',
                'PATH_INFO': self.path.split('?')[0],
                'QUERY_STRING': self.path.split('?')[1] if '?' in self.path else '',
                'CONTENT_TYPE': self.headers.get('Content-Type', ''),
                'CONTENT_LENGTH': self.headers.get('Content-Length', ''),
                'SERVER_NAME': 'localhost',
                'SERVER_PORT': '8000',
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'https',
                'wsgi.input': io.StringIO(self.rfile.read(int(self.headers.get('Content-Length', 0))).decode('utf-8')),
                'wsgi.errors': sys.stderr,
                'wsgi.multithread': False,
                'wsgi.multiprocess': True,
                'wsgi.run_once': False,
            }
            
            # Ajouter les headers HTTP
            for key, value in self.headers.items():
                key = key.replace('-', '_').upper()
                if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                    environ[f'HTTP_{key}'] = value
            
            # Fonction pour capturer la réponse
            response_data = []
            response_status = [None]
            response_headers = [None]
            
            def start_response(status, headers, exc_info=None):
                response_status[0] = status
                response_headers[0] = headers
                return response_data.append
            
            # Appeler l'application Django
            response = application(environ, start_response)
            
            # Envoyer la réponse
            status_code = int(response_status[0].split(' ')[0])
            self.send_response(status_code)
            
            for header_name, header_value in response_headers[0]:
                self.send_header(header_name, header_value)
            self.end_headers()
            
            # Écrire le contenu de la réponse
            for data in response:
                if isinstance(data, str):
                    data = data.encode('utf-8')
                self.wfile.write(data)
                
        except Exception as e:
            # En cas d'erreur, renvoyer une erreur 500
            self.send_response(500)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(f'<h1>Internal Server Error</h1><p>{str(e)}</p>'.encode('utf-8'))
