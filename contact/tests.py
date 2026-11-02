from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class ContactPageTests(TestCase):
    def test_contact_page_is_public_and_linked_in_navigation(self):
        response = self.client.get(reverse("contact:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact us")
        self.assertContains(response, reverse("contact:contact"))

    def test_contact_request_is_saved_for_admin(self):
        response = self.client.post(
            reverse("contact:contact"),
            {
                "name": "Anime Fan",
                "email": "fan@example.com",
                "subject": "Anime suggestion",
                "message": "Please add Paper Comet to the catalog.",
            },
            follow=True,
        )
        self.assertContains(response, "Your message has been sent to the app admin.")
        contact_message = ContactMessage.objects.get()
        self.assertEqual(contact_message.name, "Anime Fan")
        self.assertEqual(contact_message.subject, "Anime suggestion")
        self.assertFalse(contact_message.is_read)

    def test_invalid_contact_request_is_not_saved(self):
        response = self.client.post(
            reverse("contact:contact"),
            {
                "name": "Anime Fan",
                "email": "not-an-email",
                "subject": "Anime suggestion",
                "message": "Please add Paper Comet to the catalog.",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address.")
        self.assertFalse(ContactMessage.objects.exists())

    def test_staff_can_review_contact_inbox(self):
        ContactMessage.objects.create(
            name="Anime Fan",
            email="fan@example.com",
            subject="Anime suggestion",
            message="Please add Paper Comet.",
        )
        staff = User.objects.create_user(
            username="admin",
            password="secure-test-pass-123",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(staff)
        response = self.client.get(reverse("admin:contact_contactmessage_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anime suggestion")
