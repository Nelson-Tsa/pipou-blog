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
    """Test ultra simple pour vérifier que les POST arrivent"""
    if request.method == 'POST':
        return HttpResponse(f"🎉 POST REÇU ! Données: {dict(request.POST)}")
    
    # Générer le token CSRF correctement
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test POST</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            form {{ max-width: 400px; margin: 0 auto; }}
            input, button {{ padding: 10px; margin: 10px 0; width: 100%; }}
            button {{ background: #007cba; color: white; border: none; cursor: pointer; }}
            .success {{ background: #d4edda; padding: 15px; border-radius: 5px; color: #155724; }}
        </style>
    </head>
    <body>
        <h1>🧪 Test POST Ultra Simple</h1>
        <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <input type="text" name="test" value="hello world" placeholder="Tapez quelque chose...">
            <button type="submit">🚀 ENVOYER POST</button>
        </form>
        <p><a href="/login/">← Retour au login</a></p>
    </body>
    </html>
    """)