from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm
from django.conf import settings
from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages

from . import forms


def custom_login_view(request):
    """Vue de connexion personnalisée qui gère l'authentification par email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            User = get_user_model()
            
            # Étape 1: Vérifier si l'utilisateur existe
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, f"Aucun utilisateur trouvé avec l'email: {email}")
                return render(request, 'authentication/login.html', {'form': EmailAuthenticationForm()})
            
            # Étape 2: Vérifier le mot de passe manuellement (contourne les problèmes de backend)
            if user_obj.check_password(password):
                # Étape 3: Connecter l'utilisateur manuellement
                if user_obj.is_active:
                    login(request, user_obj)
                    messages.success(request, f"Connexion réussie ! Bienvenue {user_obj.username}")
                    return redirect(settings.LOGIN_REDIRECT_URL or '/')
                else:
                    messages.error(request, "Votre compte est désactivé.")
            else:
                messages.error(request, "Mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
    
    # Afficher le formulaire (GET ou POST avec erreurs)
    form = EmailAuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})


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