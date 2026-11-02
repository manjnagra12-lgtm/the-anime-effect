from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from catalog.models import Anime

from .forms import UserTrackerForm
from .models import UserTracker


class UserTrackerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="watcher",
            password="secure-test-pass-123",
        )
        cls.other_user = User.objects.create_user(
            username="another",
            password="secure-test-pass-123",
        )
        cls.anime = Anime.objects.create(title="Moon Harbor", total_episodes=12)
        cls.entry = UserTracker.objects.create(
            user=cls.user,
            anime=cls.anime,
            status=UserTracker.Status.WATCHING,
            current_episode=4,
        )

    def test_progress_above_episode_total_is_invalid(self):
        form = UserTrackerForm(
            {"status": UserTracker.Status.WATCHING, "current_episode": 13},
            anime=self.anime,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("current_episode", form.errors)

    def test_tracker_is_private_to_signed_in_user(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("tracker:tracker_list"))
        self.assertNotContains(response, "Moon Harbor")
        edit_response = self.client.get(reverse("tracker:tracker_edit", args=[self.entry.pk]))
        self.assertEqual(edit_response.status_code, 404)

    def test_user_can_add_anime_and_see_success_message(self):
        self.client.force_login(self.other_user)
        response = self.client.post(
            reverse("tracker:tracker_add", args=[self.anime.pk]),
            {"status": UserTracker.Status.PLAN_TO_WATCH, "current_episode": 0},
            follow=True,
        )
        self.assertContains(response, "Moon Harbor")
        self.assertContains(response, "was added to your tracker")
        self.assertTrue(
            UserTracker.objects.filter(user=self.other_user, anime=self.anime).exists()
        )

    def test_delete_is_post_only_and_scoped_to_owner(self):
        self.client.force_login(self.other_user)
        response = self.client.post(reverse("tracker:tracker_delete", args=[self.entry.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(UserTracker.objects.filter(pk=self.entry.pk).exists())
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("tracker:tracker_delete", args=[self.entry.pk]),
            follow=True,
        )
        self.assertContains(response, "Anime successfully removed from your list.")
        self.assertFalse(UserTracker.objects.filter(pk=self.entry.pk).exists())
