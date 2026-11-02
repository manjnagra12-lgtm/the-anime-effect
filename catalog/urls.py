from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.anime_list, name="anime_list"),
    path("anime/<int:pk>/", views.anime_detail, name="anime_detail"),
    path("anime/add/", views.anime_create, name="anime_create"),
    path("anime/<int:pk>/edit/", views.anime_update, name="anime_update"),
    path("anime/<int:pk>/delete/", views.anime_delete, name="anime_delete"),
]
