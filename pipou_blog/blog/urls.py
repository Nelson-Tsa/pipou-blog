from django.urls import path
from .views import BlogHome, BlogPostCreate, BlogPostEdit, BlogPostDelete, toggle_like, get_like_status, BlogPostDetail

urlpatterns = [
    path('', BlogHome.as_view(), name="index"),
    path('blog/<int:pk>/', BlogPostDetail.as_view(), name='post_detail'),
    path('blog/create/', BlogPostCreate.as_view(), name="create"),
    path('blog/edit/<int:pk>/', BlogPostEdit.as_view(), name="edit"),
    path('blog/delete/<int:pk>/', BlogPostDelete.as_view(), name="delete"),
    path('blog/like/<int:post_id>/', toggle_like, name="like"),
    path('blog/like-status/<int:post_id>/', get_like_status, name="like_status"),
]
