from django import forms

from .models import Anime


class AnimeForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = ["title", "synopsis", "total_episodes", "genres", "studio", "image"]
        widgets = {
            "synopsis": forms.Textarea(attrs={"rows": 5}),
            "genres": forms.TextInput(attrs={"placeholder": "Adventure, fantasy"}),
            "image": forms.ClearableFileInput(
                attrs={
                    "accept": ".jpg,.jpeg,.png,.gif,.webp",
                    "aria-describedby": "image-help",
                }
            ),
        }
