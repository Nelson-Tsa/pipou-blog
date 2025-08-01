from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=255, verbose_name='Titre')
  content = models.TextField(verbose_name='Contenu')
  created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  class Meta:
    verbose_name = 'Publication'
    verbose_name_plural = 'Publications'
    ordering = ['-created_at']

  def __str__(self):
    return self.title

  def get_likes_count(self):
    """Retourne le nombre total de likes pour ce post"""
    return self.likes.count()

  def is_liked_by_user(self, user):
    """Vérifie si un utilisateur a liké ce post"""
    if user.is_authenticated:
      return self.likes.filter(user=user).exists()
    return False


class Like(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    verbose_name = 'Like'
    verbose_name_plural = 'Likes'
    unique_together = ('user', 'post')
    
  def __str__(self):
    return f"{self.user} a liké {self.post.title}"