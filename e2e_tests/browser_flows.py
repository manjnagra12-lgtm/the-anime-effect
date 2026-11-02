"""Browser-based user journeys for the optional E2E suite."""

import os
from pathlib import Path

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import sync_playwright

from catalog.models import Anime
from contact.models import ContactMessage
from social.models import BlogPost, Comment
from tracker.models import UserTracker


class BrowserFlowTests(StaticLiveServerTestCase):
    def setUp(self):
        self.anime = Anime.objects.create(
            title="E2E Starlight Archive",
            synopsis="A group of friends explore the night sky.",
            total_episodes=12,
            genres="Adventure, Sci-Fi",
            studio="North Star",
        )
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.context = self.browser.new_context(
            viewport={"width": 1440, "height": 1000}
        )
        self.page = self.context.new_page()
        self.screenshot_dir = os.environ.get("E2E_SCREENSHOT_DIR")
        if self.screenshot_dir:
            self.screenshot_dir = Path(self.screenshot_dir)
            self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.close_browser()

    def close_browser(self):
        if hasattr(self, "context"):
            self.context.close()
            self.browser.close()
            self.playwright.stop()
            del self.context

    def capture(self, filename, *, full_page=True):
        if self.screenshot_dir:
            self.page.screenshot(
                path=self.screenshot_dir / filename,
                full_page=full_page,
            )

    def register(self, username):
        self.page.goto(f"{self.live_server_url}{reverse('register')}")
        self.page.locator("#id_username").fill(username)
        self.page.locator("#id_email").fill(f"{username}@example.com")
        self.page.locator("#id_password1").fill("E2E-Strong-password-2026!")
        self.page.locator("#id_password2").fill("E2E-Strong-password-2026!")
        self.page.get_by_role("button", name="Create account").click()
        self.page.wait_for_url(f"{self.live_server_url}/")
        self.assertTrue(self.page.get_by_text(f"Hi, {username}").is_visible())

    def test_registration_and_tracker_create_update_delete(self):
        self.page.goto(self.live_server_url)
        self.assertTrue(self.page.get_by_role("heading", name="Explore anime").is_visible())
        self.capture("01-discover-desktop.png")
        self.register("e2e-tracker")
        self.page.goto(self.live_server_url)
        self.page.locator(".anime-card a").filter(
            has_text=self.anime.title
        ).click()
        self.page.get_by_role("link", name="Add to my tracker").click()
        self.page.locator("#id_status").select_option(label="Watching")
        self.page.locator("#id_current_episode").fill("4")
        self.page.get_by_role("button", name="Save progress").click()
        self.page.wait_for_url(f"{self.live_server_url}{reverse('tracker:tracker_list')}")

        self.assertTrue(self.page.get_by_text("Watching").is_visible())
        self.assertTrue(self.page.get_by_text("Episode 4 of 12").is_visible())
        self.page.get_by_role("link", name="Update").click()
        self.page.locator("#id_status").select_option(label="Completed")
        self.page.locator("#id_current_episode").fill("12")
        self.page.get_by_role("button", name="Save progress").click()
        self.page.wait_for_url(f"{self.live_server_url}{reverse('tracker:tracker_list')}")
        self.assertTrue(self.page.get_by_text("Episode 12 of 12").is_visible())

        self.page.set_viewport_size({"width": 390, "height": 844})
        self.capture("02-tracker-mobile.png", full_page=False)
        self.page.once("dialog", lambda dialog: dialog.dismiss())
        self.page.get_by_role("button", name="Remove").click()
        self.assertTrue(self.page.get_by_text("Episode 12 of 12").is_visible())
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.get_by_role("button", name="Remove").click()
        self.assertTrue(self.page.get_by_text("Your tracker is waiting for a first pick.").is_visible())
        self.close_browser()
        self.assertTrue(User.objects.filter(username="e2e-tracker").exists())
        self.assertFalse(UserTracker.objects.filter(user__username="e2e-tracker").exists())

    def test_registered_user_can_publish_post_and_comment(self):
        self.register("e2e-community")
        self.page.get_by_role("link", name="Community").click()
        self.page.get_by_role("link", name="Write a post").click()
        self.page.locator("#id_content").fill("A browser-tested anime recommendation.")
        self.page.locator("#id_anime").select_option(str(self.anime.pk))
        self.page.get_by_role("button", name="Publish post").click()
        self.page.wait_for_url(f"{self.live_server_url}{reverse('social:post_list')}")
        self.assertTrue(
            self.page.get_by_text("Your post was published.").is_visible()
        )
        self.page.get_by_role("button", name="Dismiss notification").click()
        self.assertFalse(self.page.get_by_text("Your post was published.").is_visible())

        self.page.get_by_role(
            "link", name="View 0 comments · Join the discussion"
        ).click()
        post_detail_url = self.page.url
        self.page.locator("#id_content").fill("Thanks for sharing this!")
        self.page.get_by_role("button", name="Post comment").click()
        self.page.wait_for_url(post_detail_url)
        self.assertTrue(self.page.get_by_text("Thanks for sharing this!").is_visible())
        self.assertTrue(
            self.page.get_by_role("heading", name="Comments (1)").is_visible()
        )
        self.capture("03-community-post-and-comment.png")
        self.close_browser()
        self.assertEqual(BlogPost.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)

    def test_contact_request_is_submitted_to_admin_inbox(self):
        self.page.goto(f"{self.live_server_url}{reverse('contact:contact')}")
        self.page.locator("#id_name").fill("E2E Visitor")
        email = self.page.locator("#id_email")
        email.fill("not-an-email")
        self.page.get_by_role("button", name="Send message").click()
        self.assertTrue(email.evaluate("(element) => element.validity.typeMismatch"))
        self.assertEqual(self.page.url, f"{self.live_server_url}{reverse('contact:contact')}")

        email.fill("e2e-visitor@example.com")
        self.page.locator("#id_subject").fill("Please add an anime")
        self.page.locator("#id_message").fill(
            "Please consider adding E2E Starlight Archive."
        )
        self.page.get_by_role("button", name="Send message").click()
        self.page.get_by_text(
            "Your message has been sent to the app admin."
        ).wait_for()
        self.assertTrue(
            self.page.get_by_text("Your message has been sent to the app admin.").is_visible()
        )
        self.capture("04-contact-request-sent.png")
        self.close_browser()
        self.assertTrue(
            ContactMessage.objects.filter(
                email="e2e-visitor@example.com",
                subject="Please add an anime",
            ).exists()
        )

    def test_discover_reflows_and_skip_link_is_keyboard_reachable(self):
        self.page.goto(self.live_server_url)
        self.page.keyboard.press("Tab")
        self.assertEqual(
            self.page.evaluate("document.activeElement.getAttribute('href')"),
            "#main-content",
        )

        layouts = []
        for width in (320, 390, 768, 1280):
            self.page.set_viewport_size({"width": width, "height": 900})
            layouts.append(
                self.page.evaluate(
                    """() => ({
                        width: document.documentElement.clientWidth,
                        scrollWidth: document.documentElement.scrollWidth
                    })"""
                )
            )
        self.assertTrue(
            all(layout["scrollWidth"] <= layout["width"] for layout in layouts),
            layouts,
        )
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.capture("05-discover-mobile.png", full_page=False)
