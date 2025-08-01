from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Backend d'authentification personnalisé qui permet la connexion par email
    """
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        # Si email est fourni directement, l'utiliser
        if email is None:
            email = username
        
        if email is None or password is None:
            return None
        
        try:
            # Chercher l'utilisateur par email
            user = User.objects.get(Q(email=email))
        except User.DoesNotExist:
            # Exécuter le hashage du mot de passe pour éviter les attaques de timing
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Si plusieurs utilisateurs ont le même email, prendre le premier
            user = User.objects.filter(Q(email=email)).first()
        
        # Vérifier le mot de passe
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
