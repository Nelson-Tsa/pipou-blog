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


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Définir l'URL de redirection après connexion réussie"""
        return getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    def form_valid(self, form):
        """Appelée quand le formulaire est valide"""
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f'Bienvenue {user.username} !')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """Appelée quand le formulaire est invalide"""
        # Ajouter un message d'erreur pour l'utilisateur
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