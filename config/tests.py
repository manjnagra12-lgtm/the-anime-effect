from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountTests(TestCase):
    def test_registration_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newfan",
                "email": "newfan@example.com",
                "password1": "Strong-test-password-2026",
                "password2": "Strong-test-password-2026",
            },
        )
        self.assertRedirects(response, reverse("catalog:anime_list"))
        self.assertTrue(User.objects.filter(username="newfan").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            username="existing",
            email="fan@example.com",
            password="secure-test-pass-123",
        )
        response = self.client.post(
            reverse("register"),
            {
                "username": "another",
                "email": "FAN@example.com",
                "password1": "Strong-test-password-2026",
                "password2": "Strong-test-password-2026",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="another").exists())
        self.assertContains(response, "An account with this email address already exists.")

    def test_login_and_logout(self):
        User.objects.create_user(
            username="returningfan",
            password="secure-test-pass-123",
        )
        login_response = self.client.post(
            reverse("login"),
            {"username": "returningfan", "password": "secure-test-pass-123"},
        )
        self.assertRedirects(login_response, reverse("catalog:anime_list"))
        self.assertIn("_auth_user_id", self.client.session)

        logout_response = self.client.post(reverse("logout"))
        self.assertRedirects(logout_response, reverse("catalog:anime_list"))
        self.assertNotIn("_auth_user_id", self.client.session)
