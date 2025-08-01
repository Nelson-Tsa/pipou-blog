from django.contrib import admin
from .models import Post, Like

# Register your models here.
class PostAdmin(admin.ModelAdmin):
  list_display = ("title", "content")

class LikeAdmin(admin.ModelAdmin):
  list_display = ("user", "post", "created_at")
  list_filter = ("created_at", "post")
  search_fields = ("user__username", "post__title")

admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
