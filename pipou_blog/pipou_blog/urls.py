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
- <a href="/list-users/">Voir tous les utilisateurs</a>
- <a href="/list-posts/">Voir tous les articles</a>
- <a href="/admin-login/">Connexion admin personnalisée</a>

💡 Si l'admin Django ne fonctionne pas, utilisez cette interface pour gérer vos données.
        """)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {str(e)}")

def list_users(request):
    """Lister tous les utilisateurs avec détails"""
    try:
        from authentication.models import User
        
        users = User.objects.all().order_by('-date_joined')
        
        users_html = ""
        for user in users:
            users_html += f"""
            <tr>
                <td>{user.id}</td>
                <td>{user.username}</td>
                <td>{user.email}</td>
                <td>{user.first_name} {user.last_name}</td>
                <td>{'✅' if user.is_staff else '❌'}</td>
                <td>{'✅' if user.is_superuser else '❌'}</td>
                <td>{'✅' if user.is_active else '❌'}</td>
                <td>{user.date_joined.strftime('%d/%m/%Y %H:%M')}</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gestion des utilisateurs - PipouBlog</title>
            <style>
                body {{ font-family: "Arial", sans-serif; margin: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #007cba; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .header {{ background: #007cba; color: white; padding: 20px; margin: -20px -20px 20px -20px; }}
                .btn {{ display: inline-block; background: #007cba; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; margin: 5px 5px 5px 0; }}
                .btn:hover {{ background: #005a87; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>👥 Gestion des utilisateurs</h1>
                <p>Total: {users.count()} utilisateurs</p>
            </div>
            
            <div style="margin-bottom: 20px;">
                <a href="/admin-dashboard/" class="btn">← Retour au dashboard</a>
                <a href="/create-admin/" class="btn">Créer un admin</a>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nom d'utilisateur</th>
                        <th>Email</th>
                        <th>Nom complet</th>
                        <th>Staff</th>
                        <th>Superuser</th>
                        <th>Actif</th>
                        <th>Date d'inscription</th>
                    </tr>
                </thead>
                <tbody>
                    {users_html}
                </tbody>
            </table>
        </body>
        </html>
        """
        
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {str(e)}")

def list_posts(request):
    """Lister tous les articles avec détails"""
    try:
        from blog.models import Post
        
        posts = Post.objects.all().order_by('-created_at')
        
        posts_html = ""
        for post in posts:
            posts_html += f"""
            <tr>
                <td>{post.id}</td>
                <td><strong>{post.title[:50]}{'...' if len(post.title) > 50 else ''}</strong></td>
                <td>{post.user.username}</td>
                <td>{post.content[:100]}{'...' if len(post.content) > 100 else ''}</td>
                <td>{post.likes}</td>
                <td>{post.created_at.strftime('%d/%m/%Y %H:%M')}</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gestion des articles - PipouBlog</title>
            <style>
                body {{ font-family: "Arial", sans-serif; margin: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #007cba; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .header {{ background: #007cba; color: white; padding: 20px; margin: -20px -20px 20px -20px; }}
                .btn {{ display: inline-block; background: #007cba; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; margin: 5px 5px 5px 0; }}
                .btn:hover {{ background: #005a87; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📝 Gestion des articles</h1>
                <p>Total: {posts.count()} articles</p>
            </div>
            
            <div style="margin-bottom: 20px;">
                <a href="/admin-dashboard/" class="btn">← Retour au dashboard</a>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Titre</th>
                        <th>Auteur</th>
                        <th>Contenu (extrait)</th>
                        <th>Likes</th>
                        <th>Date de création</th>
                    </tr>
                </thead>
                <tbody>
                    {posts_html}
                </tbody>
            </table>
        </body>
        </html>
        """
        
        return HttpResponse(html)
        
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

def admin_custom_login(request):
    """Page de connexion admin personnalisée qui évite les redirections infinies"""
    from django.contrib.auth import authenticate, login
    from django.contrib.auth.forms import AuthenticationForm
    from django.shortcuts import redirect
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('/admin-dashboard/')  # Rediriger vers notre dashboard
            else:
                error_msg = "Utilisateur non autorisé ou identifiants incorrects"
        else:
            error_msg = "Formulaire invalide"
    else:
        form = AuthenticationForm()
        error_msg = ""
    
    # Formulaire de connexion simple
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Connexion Admin - PipouBlog</title>
        <style>
            body {{ font-family: "Arial", sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; }}
            .form-group {{ margin-bottom: 15px; }}
            label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
            input[type="text"], input[type="password"] {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }}
            button {{ background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }}
            button:hover {{ background: #005a87; }}
            .error {{ color: red; margin-bottom: 15px; }}
            .title {{ text-align: center; color: #333; margin-bottom: 30px; }}
        </style>
    </head>
    <body>
        <h1 class="title">🔐 Admin PipouBlog</h1>
        
        {f'<div class="error">{error_msg}</div>' if error_msg else ''}
        
        <form method="post">
            <div class="form-group">
                <label for="username">Nom d'utilisateur:</label><br>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Mot de passe:</label><br>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit">Se connecter</button>
        </form>
        
        <p style="margin-top: 30px; text-align: center; color: #666;">
            Identifiants par défaut: <strong>admin</strong> / <strong>admin123</strong>
        </p>
        
        <p style="text-align: center;">
            <a href="/simple-admin/">Interface simple</a> | 
            <a href="/">Retour au site</a>
        </p>
    </body>
    </html>
    """
    
    return HttpResponse(html)

def admin_dashboard(request):
    """Dashboard admin personnalisé qui remplace l'admin Django"""
    from django.contrib.auth.decorators import user_passes_test
    
    # Vérifier que l'utilisateur est connecté et est staff
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/admin-login/')
    
    try:
        users_count = User.objects.count()
        posts_count = Post.objects.count()
        superusers_count = User.objects.filter(is_superuser=True).count()
        
        # Interface d'administration complète
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard Admin - PipouBlog</title>
            <style>
                body {{ font-family: "Arial", sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .header {{ background: #007cba; color: white; padding: 20px; margin: -20px -20px 20px -20px; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .stat-number {{ font-size: 2em; font-weight: bold; color: #007cba; }}
                .actions {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }}
                .action-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .action-card h3 {{ margin-top: 0; color: #333; }}
                .btn {{ display: inline-block; background: #007cba; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; margin: 5px 5px 5px 0; }}
                .btn:hover {{ background: #005a87; }}
                .btn-danger {{ background: #dc3545; }}
                .btn-danger:hover {{ background: #c82333; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Dashboard Admin - PipouBlog</h1>
                <p>Bienvenue, {request.user.username}!</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{users_count}</div>
                    <div>Utilisateurs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{posts_count}</div>
                    <div>Articles</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{superusers_count}</div>
                    <div>Administrateurs</div>
                </div>
            </div>
            
            <div class="actions">
                <div class="action-card">
                    <h3>👥 Gestion des utilisateurs</h3>
                    <a href="/list-users/" class="btn">Voir tous les utilisateurs</a>
                    <a href="/create-admin/" class="btn">Créer un admin</a>
                </div>
                
                <div class="action-card">
                    <h3>📝 Gestion des articles</h3>
                    <a href="/list-posts/" class="btn">Voir tous les articles</a>
                </div>
                
                <div class="action-card">
                    <h3>🔧 Maintenance</h3>
                    <a href="/migrate/" class="btn">Exécuter migrations</a>
                    <a href="/load-fixtures-safe/" class="btn">Charger fixtures</a>
                    <a href="/check-static/" class="btn">Vérifier statiques</a>
                </div>
                
                <div class="action-card">
                    <h3>🌐 Navigation</h3>
                    <a href="/" class="btn">Voir le site</a>
                    <a href="/admin/logout/" class="btn btn-danger">Se déconnecter</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {str(e)}")

def admin_alternative(request):
    """Route d'admin alternative qui contourne les middlewares de sécurité"""
    try:
        from django.contrib import admin
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        
        # Rediriger vers l'admin Django mais en contournant les middlewares de sécurité
        if request.path == '/admin-alt/':
            return HttpResponseRedirect('/admin/')
        
        # Si on arrive ici, on affiche un message d'aide
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Alternative - PipouBlog</title>
            <style>
                body {{ font-family: "Arial", sans-serif; max-width: 600px; margin: 100px auto; padding: 20px; }}
                .header {{ background: #007cba; color: white; padding: 20px; margin: -20px -20px 20px -20px; text-align: center; }}
                .btn {{ display: inline-block; background: #007cba; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; margin: 5px; }}
                .btn:hover {{ background: #005a87; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 4px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔧 Admin Django Alternative</h1>
            </div>
            
            <div class="warning">
                <strong>⚠️ Note:</strong> Cette route tente de contourner les problèmes de middleware Django admin.
            </div>
            
            <h3>🔗 Options disponibles:</h3>
            <p>
                <a href="/admin/" class="btn">Admin Django Standard</a>
                <a href="/admin/login/" class="btn">Page de connexion directe</a>
            </p>
            
            <h3>🚀 Interfaces alternatives (recommandées):</h3>
            <p>
                <a href="/admin-login/" class="btn">Connexion Admin Personnalisée</a>
                <a href="/admin-dashboard/" class="btn">Dashboard Admin</a>
                <a href="/simple-admin/" class="btn">Interface Simple</a>
            </p>
            
            <div style="margin-top: 30px; text-align: center;">
                <p><strong>💡 Conseil:</strong> Si l'admin Django ne fonctionne pas, utilisez l'interface personnalisée qui est plus stable sur Vercel.</p>
                <p><a href="/">← Retour au site</a></p>
            </div>
        </body>
        </html>
        """)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {str(e)}")

def test_login_status(request):
    """Tester le statut de connexion de l'utilisateur"""
    try:
        user_info = ""
        if request.user.is_authenticated:
            user_info = f"""
            ✅ Utilisateur connecté: <strong>{request.user.username}</strong>
            📧 Email: {request.user.email}
            👤 Staff: {'✅' if request.user.is_staff else '❌'}
            🔑 Superuser: {'✅' if request.user.is_superuser else '❌'}
            """
        else:
            user_info = "❌ Aucun utilisateur connecté"
        
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Connexion - PipouBlog</title>
            <style>
                body {{ font-family: "Arial", sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
                .header {{ background: #007cba; color: white; padding: 20px; margin: -20px -20px 20px -20px; text-align: center; }}
                .status {{ background: #f8f9fa; border: 1px solid #dee2e6; padding: 20px; border-radius: 4px; margin: 20px 0; }}
                .btn {{ display: inline-block; background: #007cba; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; margin: 5px; }}
                .btn:hover {{ background: #005a87; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔍 Test de Connexion</h1>
            </div>
            
            <div class="status">
                <h3>📊 Statut actuel:</h3>
                {user_info}
            </div>
            
            <h3>🔗 Actions disponibles:</h3>
            <p>
                <a href="/login/" class="btn">Connexion Blog</a>
                <a href="/admin-login/" class="btn">Connexion Admin</a>
                <a href="/logout/" class="btn">Déconnexion</a>
            </p>
            
            <h3>🚀 Interfaces d'administration:</h3>
            <p>
                <a href="/admin-dashboard/" class="btn">Dashboard Admin</a>
                <a href="/simple-admin/" class="btn">Interface Simple</a>
                <a href="/create-admin/" class="btn">Créer Admin</a>
            </p>
            
            <div style="margin-top: 30px; text-align: center;">
                <p><a href="/">← Retour au site</a></p>
            </div>
        </body>
        </html>
        """)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {str(e)}")

def debug_login(request):
    """Diagnostic complet des problèmes de connexion"""
    try:
        from authentication.models import User
        from django.contrib.auth import authenticate
        from django.conf import settings
        
        # Informations sur les utilisateurs
        users = User.objects.all()
        users_info = ""
        for user in users:
            users_info += f"""
            <tr>
                <td>{user.username}</td>
                <td>{user.email}</td>
                <td>{'✅' if user.is_active else '❌'}</td>
                <td>{'✅' if user.is_staff else '❌'}</td>
                <td>{'✅' if user.check_password('admin123') else '❌'}</td>
            </tr>
            """
        
        # Test d'authentification
        test_auth = ""
        try:
            test_user = authenticate(username='admin', password='admin123')
            if test_user:
                test_auth = f"✅ Authentification réussie pour 'admin'"
            else:
                test_auth = "❌ Échec de l'authentification pour 'admin'"
        except Exception as e:
            test_auth = f"❌ Erreur d'authentification: {str(e)}"
        
        # Configuration actuelle
        config_info = f"""
        - LOGIN_URL: {getattr(settings, 'LOGIN_URL', 'Non défini')}
        - LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'Non défini')}
        - AUTH_USER_MODEL: {getattr(settings, 'AUTH_USER_MODEL', 'Non défini')}
        - SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', 'Non défini')}
        - CSRF_COOKIE_SECURE: {getattr(settings, 'CSRF_COOKIE_SECURE', 'Non défini')}
        """
        
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Diagnostic Connexion - PipouBlog</title>
            <style>
                body {{ font-family: "Arial", sans-serif; margin: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #007cba; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .header {{ background: #007cba; color: white; padding: 20px; margin: -20px -20px 20px -20px; }}
                .section {{ background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 15px 0; border-radius: 4px; }}
                .btn {{ display: inline-block; background: #007cba; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; margin: 5px; }}
                .btn:hover {{ background: #005a87; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔧 Diagnostic Complet de Connexion</h1>
            </div>
            
            <div class="section">
                <h3>🧪 Test d'authentification:</h3>
                <p>{test_auth}</p>
            </div>
            
            <div class="section">
                <h3>⚙️ Configuration Django:</h3>
                <pre>{config_info}</pre>
            </div>
            
            <div class="section">
                <h3>👥 Utilisateurs dans la base de données:</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Username</th>
                            <th>Email</th>
                            <th>Actif</th>
                            <th>Staff</th>
                            <th>Mot de passe 'admin123' OK</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users_info}
                    </tbody>
                </table>
                <p><strong>Total:</strong> {users.count()} utilisateurs</p>
            </div>
            
            <div class="section">
                <h3>🔗 Actions de test:</h3>
                <p>
                    <a href="/create-admin/" class="btn">Créer/Réinitialiser Admin</a>
                    <a href="/login/" class="btn">Tester Connexion</a>
                    <a href="/admin-login/" class="btn">Connexion Admin Personnalisée</a>
                </p>
            </div>
            
            <div style="margin-top: 30px; text-align: center;">
                <p><a href="/">← Retour au site</a></p>
            </div>
        </body>
        </html>
        """)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur de diagnostic: {str(e)}")

def test_login_manual(request):
    """Test de connexion manuelle pour diagnostiquer les problèmes"""
    from django.contrib.auth import authenticate, login, get_user_model
    from django.http import JsonResponse
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Test 1: Vérifier si l'utilisateur existe
        User = get_user_model()
        try:
            user_exists = User.objects.get(email=email)
            user_info = f"✅ Utilisateur trouvé: {user_exists.username} ({user_exists.email})"
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f"❌ Aucun utilisateur trouvé avec l'email: {email}",
                'users_list': list(User.objects.all().values_list('email', 'username'))
            })
        
        # Test 2: Tester l'authentification
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': f"✅ Connexion réussie pour {user.username}",
                'user_info': user_info,
                'redirect_url': '/'
            })
        else:
            # Test 3: Vérifier le mot de passe manuellement
            password_check = user_exists.check_password(password)
            return JsonResponse({
                'success': False,
                'error': f"❌ Échec de l'authentification",
                'user_info': user_info,
                'password_valid': password_check,
                'debug_info': {
                    'email_provided': email,
                    'password_provided': bool(password),
                    'user_active': user_exists.is_active,
                    'backends': settings.AUTHENTICATION_BACKENDS if hasattr(settings, 'AUTHENTICATION_BACKENDS') else 'Non configuré'
                }
            })
    
    # Formulaire de test
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test de Connexion</title>
        <style>
            body { font-family: "Arial", sans-serif; margin: 40px; }
            .form-group { margin: 15px 0; }
            input { padding: 10px; width: 300px; }
            button { padding: 10px 20px; background: #007cba; color: white; border: none; cursor: pointer; }
            .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <h1>🔍 Test de Connexion - Diagnostic</h1>
        <form id="loginForm">
            <div class="form-group">
                <label>Email:</label><br>
                <input type="email" name="email" required>
            </div>
            <div class="form-group">
                <label>Mot de passe:</label><br>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Tester la Connexion</button>
        </form>
        <div id="result"></div>
        
        <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/test-login-manual/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                    }
                });
                const data = await response.json();
                
                const resultDiv = document.getElementById('result');
                if (data.success) {
                    resultDiv.className = 'result success';
                    resultDiv.innerHTML = '<h3>✅ Succès!</h3><p>' + data.message + '</p><p>' + data.user_info + '</p>';
                    setTimeout(() => window.location.href = data.redirect_url, 2000);
                } else {
                    resultDiv.className = 'result error';
                    let html = '<h3>❌ Échec</h3><p>' + data.error + '</p>';
                    if (data.user_info) html += '<p>' + data.user_info + '</p>';
                    if (data.debug_info) {
                        html += '<h4>Informations de debug:</h4><pre>' + JSON.stringify(data.debug_info, null, 2) + '</pre>';
                    }
                    if (data.users_list) {
                        html += '<h4>Utilisateurs disponibles:</h4><ul>';
                        data.users_list.forEach(user => html += '<li>' + user[0] + ' (' + user[1] + ')</li>');
                        html += '</ul>';
                    }
                    resultDiv.innerHTML = html;
                }
            } catch (error) {
                document.getElementById('result').innerHTML = '<div class="result error">Erreur: ' + error.message + '</div>';
            }
        });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)

def show_user_emails(request):
    """Afficher les emails des utilisateurs pour faciliter les tests"""
    from django.contrib.auth import get_user_model
    
    try:
        User = get_user_model()
        users = User.objects.all()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Emails des Utilisateurs</title>
            <style>
                body { font-family: "Arial", sans-serif; margin: 40px; }
                .user { margin: 10px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
                .email { font-weight: bold; color: #007cba; }
                .username { color: #666; }
                .status { color: #28a745; }
                .inactive { color: #dc3545; }
            </style>
        </head>
        <body>
            <h1>📧 Emails des Utilisateurs</h1>
            <p>Total: {} utilisateurs</p>
        """.format(users.count())
        
        for user in users:
            status_class = "status" if user.is_active else "inactive"
            status_text = "Actif" if user.is_active else "Inactif"
            superuser_text = " (SUPERUSER)" if user.is_superuser else ""
            
            html += f"""
            <div class="user">
                <div class="email">📧 {user.email}</div>
                <div class="username">👤 Username: {user.username}</div>
                <div class="{status_class}">🔘 {status_text}{superuser_text}</div>
                <div>📅 Créé: {user.date_joined.strftime('%d/%m/%Y %H:%M')}</div>
            </div>
            """
        
        html += """
            <div style="margin-top: 30px;">
                <h3>🔧 Actions de test:</h3>
                <p>
                    <a href="/test-login-manual/" style="background: #007cba; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">Tester Connexion</a>
                    <a href="/create-admin/" style="background: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin-left: 10px;">Créer Admin</a>
                </p>
            </div>
            
            <div style="margin-top: 20px;">
                <p><a href="/">← Retour au site</a></p>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {str(e)}")

urlpatterns = [
    path('test/', simple_test, name='test'),
    path('test-template/', test_template, name='test_template'),
    path('migrate/', run_migrations, name='migrate'),
    path('load-fixtures/', load_fixtures, name='load_fixtures'),
    path('load-fixtures-safe/', load_fixtures_safe, name='load_fixtures_safe'),
    path('create-test-data/', create_test_data, name='create_test_data'),
    path('create-admin/', create_admin_user, name='create_admin'),
    path('simple-admin/', simple_admin_test, name='simple_admin'),
    path('list-users/', list_users, name='list_users'),
    path('list-posts/', list_posts, name='list_posts'),
    path('check-static/', check_static_files, name='check_static'),
    path('test-admin/', test_admin_access, name='test_admin'),
    path('test-redirect/', test_admin_redirect, name='test_redirect'),
    path('test-login/', test_login_status, name='test_login'),
    path('debug-login/', debug_login, name='debug_login'),
    path('test-login-manual/', test_login_manual, name='test_login_manual'),
    path('show-emails/', show_user_emails, name='show_emails'),
    path('admin-login/', admin_custom_login, name='admin_custom_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-alt/', admin_alternative, name='admin_alt'),
    path('', include('blog.urls')),
    path('profile/', include('user_profile.urls')),
    path('', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
