from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Like
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

class BlogHome(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "index.html"  # Template original

class BlogPostDetail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"

class BlogPostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/post_create.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BlogPostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "posts/post_update.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class BlogPostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return redirect("index")


@login_required
def get_like_status(request, post_id):
    """Vue pour récupérer l'état du like d'un post"""
    post = get_object_or_404(Post, id=post_id)
    liked = post.is_liked_by_user(request.user)
    
    return JsonResponse({
        'liked': liked,
        'likes_count': post.get_likes_count()
    })

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        liked = False
    except Like.DoesNotExist:
       Like.objects.create(user=request.user, post=post)
       liked = True
    return JsonResponse({
        "liked": liked,
        "likes_count": post.likes.count(),
        })