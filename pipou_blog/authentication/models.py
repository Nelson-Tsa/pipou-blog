from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name='Photo de profil'
    )
    
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')
    biography = models.TextField(max_length=500, null=True, blank=True, verbose_name='Biographie')
    email = models.EmailField(unique=True)

    # Annule le champ par défaut username
    #username = None

    # Indique que le champ email sera utilisé pour  l'authentification
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Personnalisation de l'affichage dans l'admin 
    class Meta:
        verbose_name = 'Utilisateur-rice'
        verbose_name_plural = 'Utilisateur-rices'
    
    def __str__(self):
        return f"{self.username} ({self.email})"
