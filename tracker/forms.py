from django import forms

from .models import UserTracker


class UserTrackerForm(forms.ModelForm):
    class Meta:
        model = UserTracker
        fields = ["status", "current_episode"]
        widgets = {"current_episode": forms.NumberInput(attrs={"min": 0})}

    def __init__(self, *args, anime=None, **kwargs):
        self.anime = anime or getattr(kwargs.get("instance"), "anime", None)
        super().__init__(*args, **kwargs)

    def clean_current_episode(self):
        episode = self.cleaned_data["current_episode"]
        if self.anime and episode > self.anime.total_episodes:
            raise forms.ValidationError(
                f"Episode progress cannot exceed {self.anime.total_episodes}."
            )
        return episode
