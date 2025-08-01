from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render

from . import forms


def login_page(request):
    form = EmailAuthenticationForm()
    message = ''
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message = "Identifiants invalides."
        else:
            message = "Veuillez corriger les erreurs ci-dessous."
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})


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