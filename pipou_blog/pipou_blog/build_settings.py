# Settings pour le build Vercel - évite les problèmes de base de données
from .settings import *

# Désactiver toutes les vérifications de base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# Désactiver les apps qui nécessitent une base de données
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
]

# Middleware minimal
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Pas de migrations pendant le build
MIGRATION_MODULES = {
    app: None for app in INSTALLED_APPS
}
