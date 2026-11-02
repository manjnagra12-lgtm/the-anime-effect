from django.urls import path

from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.tracker_list, name="tracker_list"),
    path("add/<int:anime_id>/", views.tracker_add, name="tracker_add"),
    path("<int:pk>/edit/", views.tracker_edit, name="tracker_edit"),
    path("<int:pk>/delete/", views.tracker_delete, name="tracker_delete"),
]
