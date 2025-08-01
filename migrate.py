#!/usr/bin/env python
"""
Script pour exécuter les migrations Django sur Vercel
"""
import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire du projet au Python path
project_dir = Path(__file__).resolve().parent / 'pipou_blog'
sys.path.insert(0, str(project_dir))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipou_blog.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("🔄 Exécution des migrations Django...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations terminées avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        sys.exit(1)
