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
            # Essayer de charger les fixtures avec --ignorenonexistent pour éviter les conflits
            execute_from_command_line(['manage.py', 'loaddata', 'fixtures/all_data.json', '--ignorenonexistent'])
            output = captured_output.getvalue()
            return HttpResponse(f"✅ Fixtures chargées avec succès!\n\n{output}")
        finally:
            sys.stdout = old_stdout
            
    except Exception as e:
        return HttpResponse(f"❌ Erreur lors du chargement des fixtures: {str(e)}")

def load_fixtures_safe(request):
    """Charger les fixtures en évitant les conflits de ContentType"""
    try:
        import json
        from django.contrib.contenttypes.models import ContentType
        from authentication.models import User
        from blog.models import Post
        
        # Lire le fichier de fixtures
        with open('fixtures/all_data.json', 'r', encoding='utf-8') as f:
            fixtures_data = json.load(f)
        
        results = []
        user_id_mapping = {}  # Mapping ancien_id -> nouveau_user
        
        # Première passe : créer les utilisateurs et construire le mapping
        for item in fixtures_data:
            model_name = item['model']
            
            if model_name == 'authentication.user':
                fields = item['fields']
                old_id = item['pk']
                
                user, created = User.objects.get_or_create(
                    username=fields['username'],
                    defaults={
                        'email': fields['email'],
                        'first_name': fields.get('first_name', ''),
                        'last_name': fields.get('last_name', ''),
                        'is_staff': fields.get('is_staff', False),
                        'is_superuser': fields.get('is_superuser', False),
                    }
                )
                
                # Ajouter au mapping
                user_id_mapping[old_id] = user
                
                if created:
                    results.append(f"✅ Utilisateur créé: {fields['username']} (ID: {old_id} -> {user.id})")
                else:
                    results.append(f"⚠️ Utilisateur existe déjà: {fields['username']} (ID: {old_id} -> {user.id})")
        
        # Deuxième passe : créer les articles avec le bon mapping d'utilisateurs
        for item in fixtures_data:
            model_name = item['model']
            
            if model_name == 'blog.post':
                fields = item['fields']
                old_user_id = fields['user']
                
                if old_user_id in user_id_mapping:
                    user = user_id_mapping[old_user_id]
                    
                    post, created = Post.objects.get_or_create(
                        title=fields['title'],
                        defaults={
                            'content': fields['content'],
                            'user': user,
                            'created_at': fields.get('created_at'),
                        }
                    )
                    
                    if created:
                        results.append(f"✅ Article créé: {fields['title']} (par {user.username})")
                    else:
                        results.append(f"⚠️ Article existe déjà: {fields['title']}")
                else:
                    results.append(f"❌ Utilisateur ID {old_user_id} introuvable pour l'article: {fields['title']}")
        
        return HttpResponse(f"""
🎯 Chargement sécurisé des fixtures terminé!

📊 Résultats:
{chr(10).join(results)}

📈 Statistiques:
- Utilisateurs dans le mapping: {len(user_id_mapping)}
- Total utilisateurs: {User.objects.count()}
- Total articles: {Post.objects.count()}

🔗 Liens utiles:
- Page d'accueil: /
- Administration: /admin/
        """)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur lors du chargement sécurisé: {str(e)}")

def create_test_data(request):
    """Créer des données de test directement"""
    try:
        from authentication.models import User  # Utiliser le modèle User personnalisé
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

def test_admin_access(request):
    """Tester l'accès à l'admin sans CSS"""
    try:
        from django.contrib.admin.sites import site
        from authentication.models import User  # Utiliser le modèle User personnalisé
        
        # Compter les utilisateurs
        user_count = User.objects.count()
        admin_urls = [name for name in site.urls[0].url_patterns]
        
        return HttpResponse(f"""
🔧 Test d'accès à l'admin Django:

👥 Utilisateurs dans la base: {user_count}
🔗 URLs admin disponibles: {len(admin_urls)} routes

📋 Pour accéder à l'admin:
1. Allez sur /admin/
2. Connectez-vous avec: admin / admin123
3. Si les CSS ne se chargent pas, c'est normal pour l'instant

⚠️ Si vous avez une erreur 500 sur /admin/, c'est probablement lié aux fichiers statiques.
        """)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur admin: {str(e)}")

def create_admin_user(request):
    """Créer un superuser spécifiquement pour l'admin"""
    try:
        from authentication.models import User
        
        # Créer ou récupérer le superuser admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@pipou.blog',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'PipouBlog'
            }
        )
        
        # S'assurer qu'il a les bonnes permissions
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password('admin123')
        admin_user.save()
        
        # Lister tous les superusers
        superusers = User.objects.filter(is_superuser=True)
        
        return HttpResponse(f"""
✅ Superuser admin configuré!

👤 Utilisateur: admin
🔑 Mot de passe: admin123
📧 Email: {admin_user.email}

📊 Tous les superusers:
{chr(10).join([f"- {u.username} ({u.email}) - Staff: {u.is_staff}, Super: {u.is_superuser}" for u in superusers])}

🔗 Essayez maintenant:
- Administration: /admin/
- Connexion: admin / admin123

⚠️ Si l'admin ne fonctionne toujours pas, le problème est probablement dans les templates Django admin.
        """)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur lors de la création du superuser: {str(e)}")

def simple_admin_test(request):
    """Test simple de l'interface admin sans redirection"""
    try:
        from authentication.models import User
        from blog.models import Post
        
        # Statistiques simples
        users_count = User.objects.count()
        posts_count = Post.objects.count()
        superusers = User.objects.filter(is_superuser=True)
        
        return HttpResponse(f"""
🔧 Test Admin Simple (sans redirection)

📊 Statistiques de la base de données:
- Utilisateurs: {users_count}
- Articles: {posts_count}
- Superusers: {superusers.count()}

👥 Superusers disponibles:
{chr(10).join([f"- {u.username} (Staff: {u.is_staff}, Super: {u.is_superuser})" for u in superusers])}

🔗 Actions disponibles:
- <a href="/create-admin/">Créer/Configurer admin</a>
- <a href="/admin/">Essayer l'admin Django</a>

💡 Si l'admin Django ne fonctionne pas, utilisez cette interface pour gérer vos données.
        """)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {str(e)}")

def test_admin_redirect(request):
    """Tester les redirections de l'admin"""
    import os
    from django.conf import settings
    
    info = f"""
🔧 Test des redirections Admin Django

🌐 Configuration actuelle:
- DEBUG: {settings.DEBUG}
- ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}
- SECURE_SSL_REDIRECT: {getattr(settings, 'SECURE_SSL_REDIRECT', 'Non défini')}
- LOGIN_URL: {getattr(settings, 'LOGIN_URL', 'Non défini')}
- LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')}

📋 Headers de la requête:
- HTTP_X_FORWARDED_PROTO: {request.META.get('HTTP_X_FORWARDED_PROTO', 'Non défini')}
- HTTP_HOST: {request.META.get('HTTP_HOST', 'Non défini')}
- REQUEST_SCHEME: {request.scheme}
- IS_SECURE: {request.is_secure()}

🔗 Essayez maintenant:
- <a href="/admin/">Admin Django</a> (devrait fonctionner maintenant)
- <a href="/simple-admin/">Admin Simple</a> (backup)
    """
    
    return HttpResponse(info)

urlpatterns = [
    path('test/', simple_test, name='test'),
    path('test-template/', test_template, name='test_template'),
    path('migrate/', run_migrations, name='migrate'),
    path('load-fixtures/', load_fixtures, name='load_fixtures'),
    path('load-fixtures-safe/', load_fixtures_safe, name='load_fixtures_safe'),
    path('create-test-data/', create_test_data, name='create_test_data'),
    path('create-admin/', create_admin_user, name='create_admin'),
    path('simple-admin/', simple_admin_test, name='simple_admin'),
    path('check-static/', check_static_files, name='check_static'),
    path('test-admin/', test_admin_access, name='test_admin'),
    path('test-redirect/', test_admin_redirect, name='test_redirect'),
    path('admin/', admin.site.urls),  # Réactivé avec la nouvelle configuration
    path('', include('blog.urls')),
    path('profile/', include('user_profile.urls')),
    path('', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
