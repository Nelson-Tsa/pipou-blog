from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="Email", 
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com'
        })
    )
    password = forms.CharField(
        label="Mot de passe", 
        strip=False, 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe'
        })
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = None

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email and password:
            # Tenter l'authentification avec le backend personnalisé
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                # Vérifier si l'utilisateur existe pour donner un message d'erreur plus précis
                User = get_user_model()
                try:
                    user_exists = User.objects.get(email=email)
                    if not user_exists.is_active:
                        raise forms.ValidationError("Ce compte est désactivé.")
                    else:
                        raise forms.ValidationError("Mot de passe incorrect.")
                except User.DoesNotExist:
                    raise forms.ValidationError("Aucun compte trouvé avec cet email.")
            elif not self.user.is_active:
                raise forms.ValidationError("Ce compte est désactivé.")
        
        return self.cleaned_data

    def get_user(self):
        return self.user


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Rendre first_name et last_name obligatoires
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Optionnel : personnaliser les messages d'erreur
        self.fields['first_name'].error_messages = {'required': 'Ce champ est obligatoire.'}
        self.fields['last_name'].error_messages = {'required': 'Ce champ est obligatoire.'}