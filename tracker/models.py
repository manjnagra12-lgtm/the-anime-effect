from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from catalog.models import Anime


class UserTracker(models.Model):
    class Status(models.TextChoices):
        PLAN_TO_WATCH = "Plan to Watch", "Plan to Watch"
        WATCHING = "Watching", "Watching"
        COMPLETED = "Completed", "Completed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tracker_entries",
    )
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="trackers")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLAN_TO_WATCH)
    current_episode = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["anime__title"]
        constraints = [
            models.UniqueConstraint(fields=["user", "anime"], name="unique_user_anime_tracker"),
            models.CheckConstraint(
                condition=Q(current_episode__gte=0),
                name="tracker_current_episode_nonnegative",
            ),
        ]

    def clean(self):
        super().clean()
        if self.anime_id and self.current_episode > self.anime.total_episodes:
            raise ValidationError(
                {"current_episode": f"Episode progress cannot exceed {self.anime.total_episodes}."}
            )

    def __str__(self):
        return f"{self.user} - {self.anime} ({self.status})"
