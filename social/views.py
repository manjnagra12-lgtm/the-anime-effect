from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogPostForm, CommentForm
from .models import BlogPost


def post_list(request):
    posts = (
        BlogPost.objects.select_related("author", "anime")
        .annotate(comment_count=Count("comments"))
        .order_by("-created_at")
    )
    page = Paginator(posts, 10).get_page(request.GET.get("page"))
    return render(request, "social/post_list.html", {"page": page})


def post_detail(request, pk):
    post = get_object_or_404(
        BlogPost.objects.select_related("author", "anime"),
        pk=pk,
    )
    if request.method == "POST" and not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())

    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, "Your comment was added.")
        return redirect("social:post_detail", pk=post.pk)

    comments = post.comments.select_related("author")
    return render(
        request,
        "social/post_detail.html",
        {"post": post, "comments": comments, "form": form},
    )


@login_required
def post_create(request):
    form = BlogPostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Your post was published.")
        return redirect("social:post_list")
    return render(request, "social/post_form.html", {"form": form, "heading": "Write a post"})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    form = BlogPostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your post was updated.")
        return redirect("social:post_list")
    return render(request, "social/post_form.html", {"form": form, "heading": "Edit your post"})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Your post was deleted.")
        return redirect("social:post_list")
    return render(request, "social/post_confirm_delete.html", {"post": post})
