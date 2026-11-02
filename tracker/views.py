from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Anime

from .forms import UserTrackerForm
from .models import UserTracker


@login_required
def tracker_list(request):
    entries = request.user.tracker_entries.select_related("anime")
    return render(request, "tracker/tracker_list.html", {"entries": entries})


@login_required
def tracker_add(request, anime_id):
    anime = get_object_or_404(Anime, pk=anime_id)
    existing = request.user.tracker_entries.filter(anime=anime).first()
    if existing:
        messages.info(request, "This anime is already in your tracker. You can update it below.")
        return redirect("tracker:tracker_edit", pk=existing.pk)

    form = UserTrackerForm(request.POST or None, anime=anime)
    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        entry.anime = anime
        entry.save()
        messages.success(request, f"{anime.title} was added to your tracker.")
        return redirect("tracker:tracker_list")
    return render(
        request,
        "tracker/tracker_form.html",
        {"form": form, "anime": anime, "heading": "Add to my tracker"},
    )


@login_required
def tracker_edit(request, pk):
    entry = get_object_or_404(
        UserTracker.objects.select_related("anime"),
        pk=pk,
        user=request.user,
    )
    form = UserTrackerForm(request.POST or None, instance=entry, anime=entry.anime)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{entry.anime.title} progress was updated.")
        return redirect("tracker:tracker_list")
    return render(
        request,
        "tracker/tracker_form.html",
        {"form": form, "anime": entry.anime, "heading": "Update tracker"},
    )


@login_required
def tracker_delete(request, pk):
    entry = get_object_or_404(UserTracker, pk=pk, user=request.user)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Anime successfully removed from your list.")
    return redirect("tracker:tracker_list")
