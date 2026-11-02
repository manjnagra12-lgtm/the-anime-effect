from django.contrib import admin

from .models import UserTracker


@admin.register(UserTracker)
class UserTrackerAdmin(admin.ModelAdmin):
    list_display = ["user", "anime", "status", "current_episode"]
    list_filter = ["status"]
    search_fields = ["user__username", "anime__title"]
