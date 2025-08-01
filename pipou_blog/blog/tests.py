from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Post
from django.urls import reverse

User = get_user_model()
class BlogViewTests(TestCase):
  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user(username="test", email="testuser@gmail.com", password="testpass")
    self.post = Post.objects.create(title="Test Post", content="Test Content", user=self.user)

  def test_blog_home_view(self):
    response = self.client.get(reverse("index"))

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "index.html")
    self.assertIn(self.post, response.context["posts"])

  def test_blog_post_detail_view(self):
    response = self.client.get(reverse("post_detail", args=[self.post.pk]))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "posts/post_detail.html")
    self.assertEqual(response.context["post"], self.post)

  def test_blog_post_detail_view_404(self):
    response = self.client.get(reverse("post_detail", args=[9999]))
    self.assertEqual(response.status_code, 404)

  def test_blog_post_create_view_authenticated(self):
    self.client.login(email="testuser@gmail.com", password="testpass")
    response = self.client.post(reverse("create"), {
      "title": "New Post",
      "content": "New Content"
    })

    self.assertEqual(response.status_code, 302)
    self.assertTrue(Post.objects.filter(title="New Post").exists())

  def test_blog_post_create_view_unauthenticated(self):
    response = self.client.post(reverse("create"), {
      "title": "New Post",
      "content": "New Content"
    })

    self.assertNotEqual(response.status_code, 200)

  def test_blog_post_edit_view_owner(self):
    self.client.login(email="testuser@gmail.com", password="testpass")

    response = self.client.post(reverse("edit", args=[self.post.pk]), {
      "title": "Edited Title",
      "content": "Edited Content"
    })

    self.assertEqual(response.status_code, 302)
    self.post.refresh_from_db()
    self.assertEqual(self.post.title, "Edited Title")

  def test_blog_post_edit_view_not_owner(self):
    User.objects.create_user(username="other", email="otheruser@gmail.com", password="otherpass")

    self.client.login(email="otheruser@gmail.com", password="otherpass")

    response = self.client.post(reverse("edit", args=[self.post.pk]), {
      "title": "Hacked Title",
      "content": "Hacked Title"
    })

    self.assertEqual(response.status_code, 404)

  def test_blog_post_delete_view_owner(self):
    self.client.login(email='testuser@gmail.com', password='testpass')

    response = self.client.get(reverse('delete', args=[self.post.pk]))
    self.assertEqual(response.status_code, 302)

    response = self.client.post(reverse('delete', args=[self.post.pk]), follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())


  def test_blog_post_delete_view_not_owner(self):
    User.objects.create_user(username="other2", email="other2user@gmail.com", password="other2pass")

    self.client.login(email="other2user@gmail.com", password="other2pass")

    response = self.client.post(reverse("delete", args=[self.post.pk]))

    self.assertEqual(response.status_code, 404)
    self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

