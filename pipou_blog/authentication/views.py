from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse # Import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from . import forms


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    authentication_form = EmailAuthenticationForm

    def form_valid(self, form):
        """Appelée quand le formulaire est valide"""
        login(self.request, form.get_user())
        return redirect(settings.LOGIN_REDIRECT_URL or '/')

    def form_invalid(self, form):
        """Appelée quand le formulaire est invalide"""
        # Retourner le template avec les erreurs au lieu d'un HttpResponse brut
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
        return HttpResponse(f"POST REÇU ! Données: {dict(request.POST)}")
    return HttpResponse("""
    <form method="POST">
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        <input type="text" name="test" value="hello">
        <button type="submit">TEST POST</button>
    </form>
    """.format(csrf_token=request.META.get('CSRF_COOKIE', 'no-csrf')))