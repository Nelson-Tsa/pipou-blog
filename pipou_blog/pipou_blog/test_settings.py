"""
Configuration spécifique pour les tests Django.
Ce fichier définit ses propres paramètres et utilise SQLite en mémoire pour les tests.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-test-key-not-for-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'authentication',
    'user_profile',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pipou_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pipou_blog.wsgi.application'

# Configuration de la base de données pour les tests
# Utilise la même configuration que l'environnement normal mais avec une base de test
import os
import sys
from urllib.parse import urlparse, parse_qsl

# Fonction pour vérifier si une URL est valide
def is_valid_db_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc, parsed.hostname])
    except Exception:
        return False

# Utiliser SQLite par défaut
USE_SQLITE = True

# Si DATABASE_URL est définie et semble valide, essayer d'utiliser PostgreSQL/Neon
db_url = os.getenv("DATABASE_URL")
if db_url and is_valid_db_url(db_url) and "votre_" not in db_url:
    try:
        tmpPostgres = urlparse(db_url)
        
        # Ajouter un préfixe 'test_' au nom de la base pour isoler les tests
        db_name = tmpPostgres.path.replace('/', '')
        if not db_name.startswith('test_'):
            db_name = 'test_' + db_name
        
        # Tester si la configuration est valide
        if tmpPostgres.hostname and tmpPostgres.username:
            USE_SQLITE = False
            print("Tests exécutés avec PostgreSQL/Neon", file=sys.stderr)
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': db_name,
                    'USER': tmpPostgres.username,
                    'PASSWORD': tmpPostgres.password,
                    'HOST': tmpPostgres.hostname,
                    'PORT': 5432,
                    'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
                    'TEST': {
                        'NAME': db_name,
                        'SERIALIZE': False,  # Désactiver la sérialisation pour accélérer les tests
                    },
                }
            }
    except Exception as e:
        USE_SQLITE = True
        print(f"Erreur lors de la configuration PostgreSQL: {e}. Utilisation de SQLite.", file=sys.stderr)

# Utiliser SQLite si PostgreSQL n'est pas configuré ou si une erreur s'est produite
if USE_SQLITE:
    print("Tests exécutés avec SQLite en mémoire", file=sys.stderr)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Pour gérer les fichiers média (images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Utiliser le modèle utilisateur personnalisé
AUTH_USER_MODEL = 'authentication.User'

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'

# Désactiver la migration pour les tests pour améliorer la performance
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()
