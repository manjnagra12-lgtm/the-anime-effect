from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["author", "anime", "created_at"]
    search_fields = ["author__username", "content", "anime__title"]
    list_filter = ["created_at"]
