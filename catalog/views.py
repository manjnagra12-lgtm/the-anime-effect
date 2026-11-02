from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnimeForm
from .models import Anime


def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped


def anime_list(request):
    query = request.GET.get("q", "").strip()
    anime = Anime.objects.all()
    if query:
        anime = anime.filter(
            Q(title__icontains=query)
            | Q(synopsis__icontains=query)
            | Q(genres__icontains=query)
            | Q(studio__icontains=query)
        )
    page = Paginator(anime, 12).get_page(request.GET.get("page"))
    return render(
        request,
        "catalog/anime_list.html",
        {"anime_list": page.object_list, "page": page, "query": query},
    )


def anime_detail(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    tracker_entry = None
    if request.user.is_authenticated:
        tracker_entry = request.user.tracker_entries.filter(anime=anime).first()
    return render(
        request,
        "catalog/anime_detail.html",
        {"anime": anime, "tracker_entry": tracker_entry},
    )


@staff_required
def anime_create(request):
    form = AnimeForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        anime = form.save()
        messages.success(request, f"{anime.title} was added to the catalog.")
        return redirect("catalog:anime_detail", pk=anime.pk)
    return render(request, "catalog/anime_form.html", {"form": form, "heading": "Add anime"})


@staff_required
def anime_update(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    form = AnimeForm(request.POST or None, request.FILES or None, instance=anime)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Anime details updated.")
        return redirect("catalog:anime_detail", pk=anime.pk)
    return render(request, "catalog/anime_form.html", {"form": form, "heading": "Edit anime"})


@staff_required
def anime_delete(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    if request.method == "POST":
        title = anime.title
        anime.delete()
        messages.success(request, f"{title} was removed from the catalog.")
        return redirect("catalog:anime_list")
    return render(request, "catalog/anime_confirm_delete.html", {"anime": anime})
