from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.http import HttpResponse # Import HttpResponse

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