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

def load_fixtures(request):
    """Charger les fixtures Django via le web"""
    try:
        from django.core.management import execute_from_command_line
        import io
        import sys
        
        # Capturer la sortie
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            execute_from_command_line(['manage.py', 'loaddata', 'fixtures/all_data.json'])
            output = captured_output.getvalue()
            return HttpResponse(f"✅ Fixtures chargées avec succès!\n\n{output}")
        finally:
            sys.stdout = old_stdout
            
    except Exception as e:
        return HttpResponse(f"❌ Erreur lors du chargement des fixtures: {str(e)}")

def create_test_data(request):
    """Créer des données de test directement"""
    try:
        from django.contrib.auth.models import User
        from blog.models import Post
        
        # Créer un superuser si il n'existe pas
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@pipou.blog',
                password='admin123'
            )
        else:
            admin_user = User.objects.get(username='admin')
        
        # Créer quelques articles de test
        posts_created = 0
        test_posts = [
            {
                'title': '🎉 Bienvenue sur PipouBlog !',
                'content': 'Félicitations ! Votre blog Django fonctionne parfaitement sur Vercel. Ceci est un article de test pour vérifier que tout fonctionne correctement.'
            },
            {
                'title': '🚀 Déploiement réussi sur Vercel',
                'content': 'Votre application Django a été déployée avec succès sur Vercel. Vous pouvez maintenant créer de nouveaux articles via l\'interface d\'administration.'
            },
            {
                'title': '📝 Comment créer un nouvel article',
                'content': 'Pour créer un nouvel article, rendez-vous sur /admin/ et connectez-vous avec vos identifiants. Vous pourrez ensuite gérer vos articles, utilisateurs et commentaires.'
            }
        ]
        
        for post_data in test_posts:
            if not Post.objects.filter(title=post_data['title']).exists():
                Post.objects.create(
                    title=post_data['title'],
                    content=post_data['content'],
                    user=admin_user
                )
                posts_created += 1
        
        return HttpResponse(f"""
✅ Données de test créées avec succès!

👤 Superuser créé: admin / admin123
📝 Articles créés: {posts_created}

🔗 Liens utiles:
- Page d'accueil: /
- Administration: /admin/
- Connexion admin: admin / admin123
        """)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur lors de la création des données de test: {str(e)}")

def check_static_files(request):
    """Vérifier la configuration des fichiers statiques"""
    from django.conf import settings
    import os
    
    try:
        info = f"""
📁 Configuration des fichiers statiques:

STATIC_URL: {settings.STATIC_URL}
STATIC_ROOT: {settings.STATIC_ROOT}
STATICFILES_DIRS: {getattr(settings, 'STATICFILES_DIRS', 'Non défini')}

📂 Vérification des dossiers:
- STATIC_ROOT existe: {os.path.exists(settings.STATIC_ROOT) if settings.STATIC_ROOT else 'STATIC_ROOT non défini'}

🔧 Middleware WhiteNoise: {'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE}

🌐 ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}
        """
        return HttpResponse(info)
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {str(e)}")

urlpatterns = [
    path('test/', simple_test, name='test'),
    path('test-template/', test_template, name='test_template'),
    path('migrate/', run_migrations, name='migrate'),
    path('load-fixtures/', load_fixtures, name='load_fixtures'),
    path('create-test-data/', create_test_data, name='create_test_data'),
    path('check-static/', check_static_files, name='check_static'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('profile/', include('user_profile.urls')),
    path('', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
