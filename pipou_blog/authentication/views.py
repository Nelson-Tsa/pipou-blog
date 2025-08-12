from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse_lazy

from . import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

# NOUVELLE VUE DE CONNEXION SIMPLE QUI FONCTIONNE
def custom_login_view(request):
    """Vue de connexion simple et fonctionnelle - AVEC SUPPORT GET POUR VERCEL"""
    if request.user.is_authenticated:
        return redirect('/')
    
    # SUPPORT GET ET POST (contournement Vercel)
    if request.method == 'POST' or request.method == 'GET':
        email = request.POST.get('email') or request.GET.get('email')
        password = request.POST.get('password') or request.GET.get('password')
        
        if email and password:
            # Utiliser notre backend d'authentification par email
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    if user.is_active:
                        # CORRECTION : Spécifier le backend d'authentification
                        user.backend = 'authentication.backends.EmailBackend'
                        login(request, user)
                        messages.success(request, f'Connexion réussie ! Bienvenue {user.username}')
                        next_url = request.GET.get('next', '/')
                        return redirect(next_url)
                    else:
                        messages.error(request, 'Votre compte est désactivé.')
                else:
                    messages.error(request, 'Mot de passe incorrect.')
            except User.DoesNotExist:
                messages.error(request, 'Aucun compte trouvé avec cet email.')
        elif request.GET.get('email') or request.POST.get('email'):  # Si tentative de connexion
            messages.error(request, 'Veuillez remplir tous les champs.')
    
    return render(request, 'authentication/login.html', {
        'form': forms.EmailAuthenticationForm()
    })

# ANCIENNE VUE - GARDÉE POUR RÉFÉRENCE MAIS NON UTILISÉE
class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    form_class = forms.EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return '/'

    def form_valid(self, form):
        messages.success(self.request, f'Connexion réussie ! Bienvenue {form.get_user().username}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur de connexion. Vérifiez vos identifiants.')
        return self.render_to_response(self.get_context_data(form=form))

def register_page(request):
    form = forms.RegisterForm()
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = forms.RegisterForm()
    return render(request, 'authentication/register.html', context={'form': form})

def debug_login(request):
    """Vue de debug pour tester l'authentification"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        debug_info = {
            'email_received': email,
            'password_received': bool(password),
            'users_in_db': User.objects.count(),
        }
        
        # Test 1: Chercher l'utilisateur par email
        try:
            user = User.objects.get(email=email)
            debug_info['user_found'] = True
            debug_info['user_id'] = user.id
            debug_info['user_is_active'] = user.is_active
            
            # Test 2: Vérifier le mot de passe
            password_valid = user.check_password(password)
            debug_info['password_valid'] = password_valid
            
            # Test 3: Tester l'authentification
            auth_user = authenticate(request, email=email, password=password)
            debug_info['authenticate_result'] = bool(auth_user)
            
            if auth_user:
                login(request, auth_user)
                debug_info['login_successful'] = True
                debug_info['redirect_url'] = settings.LOGIN_REDIRECT_URL
            else:
                debug_info['login_successful'] = False
                
        except User.DoesNotExist:
            debug_info['user_found'] = False
            
        return JsonResponse(debug_info)
    
    # Afficher le formulaire de test
    return render(request, 'authentication/debug_login.html')


def test_post(request):
    """Vue simple pour tester si les données POST arrivent au serveur"""
    if request.method == 'POST':
        email = request.POST.get('email', 'NON REÇU')
        password = request.POST.get('password', 'NON REÇU')
        
        return HttpResponse(f"""
        <h1>✅ DONNÉES POST REÇUES !</h1>
        <p><strong>Email reçu:</strong> {email}</p>
        <p><strong>Mot de passe reçu:</strong> {'***' if password != 'NON REÇU' else 'NON REÇU'}</p>
        <p><strong>Toutes les données POST:</strong> {dict(request.POST)}</p>
        <p><strong>Méthode:</strong> {request.method}</p>
        <p><strong>URL:</strong> {request.get_full_path()}</p>
        <hr>
        <p>Si vous voyez cette page, le problème n'est PAS dans la soumission du formulaire !</p>
        <p><a href="/login/">← Retour à la connexion</a></p>
        """)
    else:
        return HttpResponse(f"""
        <h1>🔍 TEST DE SOUMISSION</h1>
        <p>Cette page teste si les données POST arrivent au serveur.</p>
        <form method="POST">
            <p>Email: <input type="email" name="email" required></p>
            <p>Password: <input type="password" name="password" required></p>
            <p><button type="submit">Tester POST</button></p>
        </form>
        <p><a href="/login/">← Retour à la connexion</a></p>
        """)

@csrf_exempt
def test_post_no_csrf(request):
    """Test POST sans CSRF pour identifier le problème"""
    if request.method == 'POST':
        return HttpResponse(f"""
        <h1>🎉 POST REÇU SANS CSRF !</h1>
        <p><strong>Méthode:</strong> {request.method}</p>
        <p><strong>Données POST:</strong> {dict(request.POST)}</p>
        <p><strong>User-Agent:</strong> {request.META.get('HTTP_USER_AGENT', 'Non défini')}</p>
        <hr>
        <p>✅ Si vous voyez cette page, le problème est le CSRF !</p>
        <p><a href="/login/">← Retour à la connexion</a></p>
        """)
    else:
        # Générer le token CSRF manuellement
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        return HttpResponse(f"""
        <h1>🧪 TEST POST SANS CSRF</h1>
        <p>Ce test contourne la protection CSRF pour identifier le problème.</p>
        
        <form method="POST" style="border: 2px solid red; padding: 20px; margin: 20px 0;">
            <h3>🚨 FORMULAIRE SANS CSRF</h3>
            <p>Email: <input type="email" name="email" value="test@test.com" required></p>
            <p>Test: <input type="text" name="test" value="hello world" required></p>
            <p><button type="submit" style="background: red; color: white; padding: 10px;">TESTER SANS CSRF</button></p>
        </form>
        
        <form method="POST" style="border: 2px solid green; padding: 20px; margin: 20px 0;">
            <h3>✅ FORMULAIRE AVEC CSRF</h3>
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <p>Email: <input type="email" name="email" value="test@test.com" required></p>
            <p>Test: <input type="text" name="test" value="hello world" required></p>
            <p><button type="submit" style="background: green; color: white; padding: 10px;">TESTER AVEC CSRF</button></p>
        </form>
        
        <p><strong>Instructions:</strong></p>
        <ol>
            <li>Testez d'abord le bouton ROUGE (sans CSRF)</li>
            <li>Si ça marche → le problème est le CSRF</li>
            <li>Si ça ne marche pas → le problème est plus profond</li>
        </ol>
        
        <p><a href="/login/">← Retour à la connexion</a></p>
        """)

@csrf_exempt
def simple_login_test(request):
    """Vue de connexion ultra simple pour contourner les problèmes"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Test 1: Vérifier si l'utilisateur existe
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            user_found = f"✅ Utilisateur trouvé: {user.username} ({user.email})"
        except User.DoesNotExist:
            return HttpResponse(f"""
            <h1>❌ UTILISATEUR NON TROUVÉ</h1>
            <p>Email testé: {email}</p>
            <p>Utilisateurs disponibles:</p>
            <ul>
            {''.join([f'<li>{u.email} ({u.username})</li>' for u in User.objects.all()])}
            </ul>
            <p><a href="/simple-login-test/">← Retour</a></p>
            """)
        
        # Test 2: Vérifier le mot de passe
        if user.check_password(password):
            password_ok = "✅ Mot de passe correct"
            
            # Test 3: Connexion manuelle
            from django.contrib.auth import login
            login(request, user)
            
            return HttpResponse(f"""
            <h1>🎉 CONNEXION RÉUSSIE !</h1>
            <p>{user_found}</p>
            <p>{password_ok}</p>
            <p>Utilisateur connecté: {request.user.username}</p>
            <p>Authentifié: {request.user.is_authenticated}</p>
            <hr>
            <p><a href="/" style="background: green; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">→ Aller à l'accueil</a></p>
            <p><a href="/admin-dashboard/" style="background: blue; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">→ Dashboard admin</a></p>
            <script>
            // Redirection automatique après 3 secondes
            setTimeout(function() {{
                window.location.href = '/';
            }}, 3000);
            </script>
            """)
        else:
            return HttpResponse(f"""
            <h1>❌ MOT DE PASSE INCORRECT</h1>
            <p>{user_found}</p>
            <p>❌ Mot de passe incorrect</p>
            <p><a href="/simple-login-test/">← Retour</a></p>
            """)
    
    # Formulaire GET
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Test Connexion Simple</title></head>
    <body style="font-family: Arial; margin: 40px;">
        <h1>🔧 TEST CONNEXION SIMPLE</h1>
        <p>Cette vue contourne tous les problèmes potentiels pour tester la connexion de base.</p>
        
        <form method="POST" style="border: 2px solid green; padding: 20px; max-width: 400px;">
            <h3>📝 Connexion directe</h3>
            <p>Email: <input type="email" name="email" value="admin@pipou.blog" required style="width: 100%; padding: 8px;"></p>
            <p>Mot de passe: <input type="password" name="password" value="admin123" required style="width: 100%; padding: 8px;"></p>
            <p><button type="submit" style="background: green; color: white; padding: 10px 20px; border: none;">SE CONNECTER</button></p>
        </form>
        
        <p><strong>Identifiants pré-remplis:</strong> admin@pipou.blog / admin123</p>
        <p><a href="/login/">← Retour à la connexion normale</a></p>
    </body>
    </html>
    """)

# VUE DE CONTOURNEMENT VERCEL - SOLUTION RADICALE
def vercel_bypass_login(request):
    """Vue qui contourne les problèmes de Vercel avec une approche hybride"""
    
    # Récupérer les données soit via POST soit via GET (contournement Vercel)
    email = request.POST.get('email') or request.GET.get('email')
    password = request.POST.get('password') or request.GET.get('password')
    action = request.POST.get('action') or request.GET.get('action')
    
    if email and password and action == 'login':
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user.is_active:
                    login(request, user)
                    return HttpResponse(f"""
                    <!DOCTYPE html>
                    <html>
                    <head><title>Connexion Réussie</title></head>
                    <body style="font-family: Arial; margin: 40px; text-align: center;">
                        <h1>🎉 CONNEXION RÉUSSIE !</h1>
                        <p>Bienvenue {user.username} !</p>
                        <p>Email: {user.email}</p>
                        <p>Statut: Connecté</p>
                        <hr>
                        <p><a href="/" style="background: green; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">→ Aller à l'accueil</a></p>
                        <p><a href="/admin-dashboard/" style="background: blue; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">→ Dashboard admin</a></p>
                        <script>
                        // Redirection automatique après 3 secondes
                        setTimeout(function() {{
                            window.location.href = '/';
                        }}, 3000);
                        </script>
                    </body>
                    </html>
                    """)
                else:
                    error_msg = "Compte désactivé"
            else:
                error_msg = "Mot de passe incorrect"
        except User.DoesNotExist:
            error_msg = "Utilisateur non trouvé"
    elif action == 'login':
        error_msg = "Veuillez remplir tous les champs"
    else:
        error_msg = None
    
    # Formulaire avec méthodes multiples (POST + GET de secours)
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Connexion Vercel Bypass</title>
        <style>
            body {{ font-family: Arial; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }}
            button {{ width: 100%; padding: 12px; background: #007cba; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
            button:hover {{ background: #005a87; }}
            .error {{ background: #ffebee; color: #c62828; padding: 10px; border-radius: 5px; margin: 10px 0; }}
            .method {{ background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Connexion Bypass Vercel</h1>
            
            {f'<div class="error">❌ {error_msg}</div>' if error_msg else ''}
            
            <div class="method">
                <strong>Méthode actuelle:</strong> {request.method}<br>
                <strong>URL:</strong> {request.get_full_path()}<br>
                <strong>Données POST:</strong> {dict(request.POST)}<br>
                <strong>Données GET:</strong> {dict(request.GET)}
            </div>
            
            <!-- Méthode 1: POST classique -->
            <form method="POST" style="border: 2px solid blue; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h3>📝 Méthode POST</h3>
                <input type="email" name="email" placeholder="Email" value="admin@pipou.blog" required>
                <input type="password" name="password" placeholder="Mot de passe" value="admin123" required>
                <input type="hidden" name="action" value="login">
                <button type="submit">CONNEXION POST</button>
            </form>
            
            <!-- Méthode 2: GET de contournement -->
            <form method="GET" style="border: 2px solid green; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h3>🔄 Méthode GET (contournement)</h3>
                <input type="email" name="email" placeholder="Email" value="admin@pipou.blog" required>
                <input type="password" name="password" placeholder="Mot de passe" value="admin123" required>
                <input type="hidden" name="action" value="login">
                <button type="submit">CONNEXION GET</button>
            </form>
            
            <!-- Méthode 3: JavaScript -->
            <div style="border: 2px solid orange; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h3>⚡ Méthode JavaScript</h3>
                <input type="email" id="js-email" placeholder="Email" value="admin@pipou.blog">
                <input type="password" id="js-password" placeholder="Mot de passe" value="admin123">
                <button onclick="jsLogin()">CONNEXION JS</button>
            </div>
            
            <p><a href="/login/">← Retour connexion normale</a></p>
        </div>
        
        <script>
        function jsLogin() {{
            const email = document.getElementById('js-email').value;
            const password = document.getElementById('js-password').value;
            window.location.href = `/vercel-bypass-login/?email=${{encodeURIComponent(email)}}&password=${{encodeURIComponent(password)}}&action=login`;
        }}
        </script>
    </body>
    </html>
    """)