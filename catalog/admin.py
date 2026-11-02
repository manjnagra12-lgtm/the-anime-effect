from django.contrib import admin

from .models import Anime


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ["title", "studio", "total_episodes"]
    search_fields = ["title", "synopsis", "genres", "studio"]
    list_filter = ["studio"]
