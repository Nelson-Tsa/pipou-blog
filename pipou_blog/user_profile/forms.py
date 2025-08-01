from django import forms
from authentication.models import User

class CustomClearableFileInput(forms.ClearableFileInput):
    """
    Widget personnalisé pour le champ de fichier/image qui utilise notre template.
    """
    template_name = 'user_profile/custom_clearable_file_input.html'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'biography', 'profile_picture']
        widgets = {
            'profile_picture': CustomClearableFileInput(),
        }
