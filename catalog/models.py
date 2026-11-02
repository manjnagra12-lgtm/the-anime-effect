from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.templatetags.static import static


def validate_image_size(image):
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Image file size must be 5 MB or less.")


class Anime(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    synopsis = models.TextField(blank=True)
    total_episodes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    genres = models.CharField(max_length=255, blank=True)
    studio = models.CharField(max_length=150, blank=True)
    image = models.ImageField(
        upload_to="anime/",
        blank=True,
        validators=[validate_image_size],
    )

    class Meta:
        ordering = ["title"]
        constraints = [
            models.CheckConstraint(
                condition=Q(total_episodes__gte=1),
                name="anime_total_episodes_positive",
            )
        ]

    def __str__(self):
        return self.title

    @property
    def cover_image_url(self):
        if not self.image:
            return ""
        if self.image.storage.exists(self.image.name):
            return self.image.url

        bundled_cover = f"images/{self.image.name.rsplit('/', 1)[-1]}"
        if finders.find(bundled_cover):
            return static(bundled_cover)
        return ""
