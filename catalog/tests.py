from io import BytesIO
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Anime


class AnimeCatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.anime = Anime.objects.create(
            title="Starlight Archive",
            synopsis="A group of friends explore the night sky.",
            total_episodes=12,
            genres="Adventure, Sci-Fi",
            studio="North Star",
        )

    def test_catalog_lists_and_searches_anime(self):
        response = self.client.get(reverse("catalog:anime_list"), {"q": "North Star"})
        self.assertContains(response, "Starlight Archive")
        self.assertEqual(list(response.context["anime_list"]), [self.anime])

    def test_anime_detail_shows_catalog_information(self):
        response = self.client.get(reverse("catalog:anime_detail", args=[self.anime.pk]))
        self.assertContains(response, "A group of friends")
        self.assertContains(response, "Adventure, Sci-Fi")
        self.assertContains(response, "North Star")

    def test_missing_uploaded_cover_uses_matching_bundled_static_cover(self):
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            for filename in (
                "black_clover.webp",
                "ATTACKONTITAN.jpg",
                "solo.webp",
                "solo_s6qyDKK.webp",
            ):
                with self.subTest(filename=filename):
                    self.anime.image.name = f"anime/{filename}"
                    self.anime.save(update_fields=["image"])

                    list_response = self.client.get(reverse("catalog:anime_list"))
                    detail_response = self.client.get(
                        reverse("catalog:anime_detail", args=[self.anime.pk])
                    )

                    self.assertContains(list_response, f"/static/images/{filename}")
                    self.assertContains(detail_response, f"/static/images/{filename}")

    def test_non_staff_cannot_manage_catalog(self):
        User.objects.create_user(username="fan", password="secure-test-pass-123")
        self.client.login(username="fan", password="secure-test-pass-123")
        response = self.client.get(reverse("catalog:anime_create"))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_create_catalog_entry(self):
        staff = User.objects.create_user(
            username="editor",
            password="secure-test-pass-123",
            is_staff=True,
        )
        self.client.force_login(staff)
        response = self.client.post(
            reverse("catalog:anime_create"),
            {
                "title": "Cloud Lantern",
                "synopsis": "A story above the city.",
                "total_episodes": 8,
                "genres": "Fantasy",
                "studio": "Moon Studio",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Anime.objects.filter(title="Cloud Lantern").exists())

    def test_staff_can_edit_and_delete_catalog_entry(self):
        staff = User.objects.create_user(
            username="catalog-admin",
            password="secure-test-pass-123",
            is_staff=True,
        )
        self.client.force_login(staff)
        edit_response = self.client.post(
            reverse("catalog:anime_update", args=[self.anime.pk]),
            {
                "title": "Starlight Archive: Updated",
                "synopsis": self.anime.synopsis,
                "total_episodes": self.anime.total_episodes,
                "genres": self.anime.genres,
                "studio": self.anime.studio,
            },
        )
        self.assertEqual(edit_response.status_code, 302)
        self.anime.refresh_from_db()
        self.assertEqual(self.anime.title, "Starlight Archive: Updated")

        delete_response = self.client.post(
            reverse("catalog:anime_delete", args=[self.anime.pk])
        )
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Anime.objects.filter(pk=self.anime.pk).exists())

    def test_staff_can_upload_anime_cover_image(self):
        image_buffer = BytesIO()
        Image.new("RGB", (4, 4), color="purple").save(image_buffer, format="PNG")
        image_file = SimpleUploadedFile(
            "cover.png",
            image_buffer.getvalue(),
            content_type="image/png",
        )
        staff = User.objects.create_user(
            username="image-editor",
            password="secure-test-pass-123",
            is_staff=True,
        )
        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                self.client.force_login(staff)
                response = self.client.post(
                    reverse("catalog:anime_create"),
                    {
                        "title": "Painted Skies",
                        "synopsis": "A story in color.",
                        "total_episodes": 8,
                        "genres": "Fantasy",
                        "studio": "Moon Studio",
                        "image": image_file,
                    },
                )
                self.assertEqual(response.status_code, 302)
                anime = Anime.objects.get(title="Painted Skies")
                self.assertTrue(anime.image)
                self.assertTrue(anime.image.storage.exists(anime.image.name))
                self.assertContains(
                    self.client.get(reverse("catalog:anime_list")),
                    "/media/anime/",
                )
