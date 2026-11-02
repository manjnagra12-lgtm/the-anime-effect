from django import forms

from .models import BlogPost, Comment


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["content", "anime"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 5,
                    "maxlength": BlogPost.MAX_CONTENT_LENGTH,
                    "placeholder": "Share what you think...",
                }
            ),
            "anime": forms.Select(attrs={"aria-label": "Related anime (optional)"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "maxlength": Comment.MAX_CONTENT_LENGTH,
                    "placeholder": "Add to the conversation...",
                }
            ),
        }
