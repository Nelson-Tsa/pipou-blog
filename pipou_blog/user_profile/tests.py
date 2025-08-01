from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from authentication.models import User
from user_profile.forms import UserProfileForm
import tempfile
import os
from PIL import Image
from io import BytesIO

# Créer un répertoire temporaire pour les tests
TEST_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class UserProfileViewsTestCase(TestCase):
    """Tests pour les vues du module user_profile"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            biography='Biographie de test'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123',
            first_name='Other',
            last_name='User'
        )
    
    def test_profile_view_authenticated_user(self):
        """Test de la vue profil pour un utilisateur authentifié"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.biography)
    
    def test_profile_view_unauthenticated_user(self):
        """Test de la vue profil pour un utilisateur non authentifié"""
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user.id}))
        
        # Doit rediriger vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_profile_view_nonexistent_user(self):
        """Test de la vue profil pour un utilisateur inexistant"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('profile', kwargs={'user_id': 9999}))
        
        self.assertEqual(response.status_code, 404)
    
    def test_profile_view_other_user(self):
        """Test de la vue profil d'un autre utilisateur"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('profile', kwargs={'user_id': self.other_user.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.other_user.username)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class EditProfileViewTestCase(TestCase):
    """Tests pour la vue de modification du profil"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            biography='Biographie originale'
        )
    
    def test_edit_profile_view_get_authenticated(self):
        """Test GET de la vue d'édition de profil pour un utilisateur authentifié"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('edit_profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, 'Biographie originale')
        self.assertIsInstance(response.context['form'], UserProfileForm)
    
    def test_edit_profile_view_get_unauthenticated(self):
        """Test GET de la vue d'édition de profil pour un utilisateur non authentifié"""
        response = self.client.get(reverse('edit_profile'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_edit_profile_view_post_valid_data(self):
        """Test POST de la vue d'édition de profil avec des données valides"""
        self.client.login(email='test@example.com', password='testpass123')
        
        form_data = {
            'username': 'nouveaunom',
            'first_name': 'Nouveau',
            'last_name': 'Nom',
            'email': 'nouveau@example.com',
            'biography': 'Nouvelle biographie mise à jour'
        }
        
        response = self.client.post(reverse('edit_profile'), data=form_data)
        
        # Doit rediriger vers la page de profil
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('profile', kwargs={'user_id': self.user.id}))
        
        # Vérifier que les données ont été mises à jour
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'nouveaunom')
        self.assertEqual(self.user.first_name, 'Nouveau')
        self.assertEqual(self.user.last_name, 'Nom')
        self.assertEqual(self.user.email, 'nouveau@example.com')
        self.assertEqual(self.user.biography, 'Nouvelle biographie mise à jour')
    
    def test_edit_profile_view_post_invalid_data(self):
        """Test POST de la vue d'édition de profil avec des données invalides"""
        self.client.login(email='test@example.com', password='testpass123')
        
        # Email invalide
        form_data = {
            'username': 'nouveaunom',
            'first_name': 'Nouveau',
            'last_name': 'Nom',
            'email': 'email_invalide',
            'biography': 'Nouvelle biographie'
        }
        
        response = self.client.post(reverse('edit_profile'), data=form_data)
        
        # Doit rester sur la page d'édition
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'email_invalide')
        
        # Vérifier que les données n'ont pas été mises à jour
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@example.com')
    
    def test_edit_profile_with_profile_picture(self):
        """Test de modification du profil avec une image de profil"""
        self.client.login(email='test@example.com', password='testpass123')
        
        # Créer une image simple
        image = Image.new('RGB', (10, 10), color='red')
        image_file = BytesIO()
        image.save(image_file, format='JPEG')
        image_content = image_file.getvalue()
        
        # Créer le fichier uploadé
        uploaded_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_content,
            content_type='image/jpeg'
        )
        
        # Préparer les données du formulaire
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'biography': 'Biographie avec image',
            'profile_picture': uploaded_file
        }
        
        response = self.client.post(reverse('edit_profile'), data=form_data)
        
        # Vérifier la réponse
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que l'image a été sauvegardée
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.profile_picture.name)
        self.assertIn('profile_pictures/', self.user.profile_picture.name)
        
        # Nettoyer le fichier si il existe
        if self.user.profile_picture and hasattr(self.user.profile_picture, 'path'):
            try:
                if os.path.exists(self.user.profile_picture.path):
                    os.unlink(self.user.profile_picture.path)
            except (OSError, ValueError):
                # Ignorer les erreurs de nettoyage dans les tests
                pass


class DeleteAccountViewTestCase(TestCase):
    """Tests pour la vue de suppression de compte"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_delete_account_view_get_authenticated(self):
        """Test GET de la vue de suppression de compte (doit rediriger)"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('delete_account'))
        
        # Doit rediriger vers edit_profile
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('edit_profile'))
    
    def test_delete_account_view_get_unauthenticated(self):
        """Test GET de la vue de suppression de compte pour un utilisateur non authentifié"""
        response = self.client.get(reverse('delete_account'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_delete_account_view_post_authenticated(self):
        """Test POST de la vue de suppression de compte pour un utilisateur authentifié"""
        self.client.login(email='test@example.com', password='testpass123')
        user_id = self.user.id
        
        response = self.client.post(reverse('delete_account'))
        
        # Doit rediriger vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
        
        # Vérifier que l'utilisateur a été supprimé
        self.assertFalse(User.objects.filter(id=user_id).exists())
    
    def test_delete_account_view_post_unauthenticated(self):
        """Test POST de la vue de suppression de compte pour un utilisateur non authentifié"""
        response = self.client.post(reverse('delete_account'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        
        # Vérifier que l'utilisateur n'a pas été supprimé
        self.assertTrue(User.objects.filter(id=self.user.id).exists())


class UserProfileFormTestCase(TestCase):
    """Tests pour le formulaire UserProfileForm"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_profile_form_valid_data(self):
        """Test du formulaire avec des données valides"""
        form_data = {
            'username': 'nouveaunom',
            'first_name': 'Nouveau',
            'last_name': 'Nom',
            'email': 'nouveau@example.com',
            'biography': 'Nouvelle biographie'
        }
        
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_user_profile_form_invalid_email(self):
        """Test du formulaire avec un email invalide"""
        form_data = {
            'username': 'nouveaunom',
            'first_name': 'Nouveau',
            'last_name': 'Nom',
            'email': 'email_invalide',
            'biography': 'Nouvelle biographie'
        }
        
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_user_profile_form_empty_required_fields(self):
        """Test du formulaire avec des champs requis vides"""
        form_data = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'biography': 'Biographie optionnelle'
        }
        
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
    
    def test_user_profile_form_fields(self):
        """Test que le formulaire contient les bons champs"""
        form = UserProfileForm(instance=self.user)
        expected_fields = ['username', 'first_name', 'last_name', 'email', 'biography', 'profile_picture']
        
        for field in expected_fields:
            self.assertIn(field, form.fields)
    
    def test_user_profile_form_save(self):
        """Test de la sauvegarde du formulaire"""
        form_data = {
            'username': 'nouveaunom',
            'first_name': 'Nouveau',
            'last_name': 'Nom',
            'email': 'nouveau@example.com',
            'biography': 'Biographie mise à jour'
        }
        
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        
        saved_user = form.save()
        
        self.assertEqual(saved_user.username, 'nouveaunom')
        self.assertEqual(saved_user.first_name, 'Nouveau')
        self.assertEqual(saved_user.last_name, 'Nom')
        self.assertEqual(saved_user.email, 'nouveau@example.com')
        self.assertEqual(saved_user.biography, 'Biographie mise à jour')
    
    def test_user_profile_form_with_image(self):
        """Test du formulaire avec une image de profil"""
        # Créer une image temporaire
        image = Image.new('RGB', (100, 100), color='blue')
        
        # Créer un fichier temporaire en mémoire
        image_file = BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        
        uploaded_file = SimpleUploadedFile(
            name='test_profile.jpg',
            content=image_file.getvalue(),
            content_type='image/jpeg'
        )
        
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'biography': 'Biographie avec image'
        }
        
        form = UserProfileForm(
            data=form_data, 
            files={'profile_picture': uploaded_file}, 
            instance=self.user
        )
        
        self.assertTrue(form.is_valid())
        
        saved_user = form.save()
        self.assertTrue(saved_user.profile_picture)
        self.assertIn('profile_pictures/', saved_user.profile_picture.name)
        
        # Nettoyer les fichiers temporaires
        if saved_user.profile_picture and hasattr(saved_user.profile_picture, 'path'):
            try:
                if os.path.exists(saved_user.profile_picture.path):
                    os.unlink(saved_user.profile_picture.path)
            except (OSError, ValueError):
                # Ignorer les erreurs de nettoyage dans les tests
                pass


class UserProfileIntegrationTestCase(TestCase):
    """Tests d'intégration pour le module user_profile"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            biography='Biographie originale'
        )
    
    def test_complete_profile_workflow(self):
        """Test du workflow complet : connexion -> modification -> visualisation"""
        # 1. Connexion
        login_success = self.client.login(email='test@example.com', password='testpass123')
        self.assertTrue(login_success)
        
        # 2. Visualisation du profil initial
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Biographie originale')
        
        # 3. Modification du profil
        form_data = {
            'username': 'testuser_modifie',
            'first_name': 'Test Modifié',
            'last_name': 'User Modifié',
            'email': 'test_modifie@example.com',
            'biography': 'Biographie modifiée'
        }
        
        response = self.client.post(reverse('edit_profile'), data=form_data)
        self.assertEqual(response.status_code, 302)
        
        # 4. Vérification des modifications
        response = self.client.get(reverse('profile', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser_modifie')
        self.assertContains(response, 'Test Modifié')
        self.assertContains(response, 'Biographie modifiée')
        self.assertNotContains(response, 'Biographie originale')
    
    def test_profile_deletion_workflow(self):
        """Test du workflow de suppression de compte"""
        # 1. Connexion
        self.client.login(email='test@example.com', password='testpass123')
        user_id = self.user.id
        
        # 2. Vérification que l'utilisateur existe
        self.assertTrue(User.objects.filter(id=user_id).exists())
        
        # 3. Suppression du compte
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
        
        # 4. Vérification que l'utilisateur a été supprimé
        self.assertFalse(User.objects.filter(id=user_id).exists())
        
        # 5. Vérification que l'utilisateur est déconnecté
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
