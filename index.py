import os
import sys
from pathlib import Path

# Ajouter le répertoire du projet au Python path
project_dir = Path(__file__).resolve().parent / 'pipou_blog'
sys.path.insert(0, str(project_dir))

# Configurer les variables d'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipou_blog.settings')

# Initialiser Django
import django
django.setup()

from django.core.wsgi import get_wsgi_application

# Obtenir l'application WSGI Django
app = get_wsgi_application()

# Export pour Vercel - l'application WSGI directement
handler = app
