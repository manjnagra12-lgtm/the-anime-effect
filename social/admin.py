from django.contrib import admin

from .models import BlogPost, Comment


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["author", "anime", "created_at"]
    search_fields = ["author__username", "content", "anime__title"]
    list_filter = ["created_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "post", "created_at"]
    search_fields = ["author__username", "content", "post__content"]
    list_filter = ["created_at"]
