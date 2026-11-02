from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models

from catalog.models import Anime


class BlogPost(models.Model):
    MAX_CONTENT_LENGTH = 1000

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    anime = models.ForeignKey(
        Anime,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    content = models.TextField(validators=[MaxLengthValidator(MAX_CONTENT_LENGTH)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post by {self.author} on {self.created_at:%Y-%m-%d}"


class Comment(models.Model):
    MAX_CONTENT_LENGTH = 1000

    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_comments",
    )
    content = models.TextField(validators=[MaxLengthValidator(MAX_CONTENT_LENGTH)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
