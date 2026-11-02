from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from catalog.models import Anime

from .forms import BlogPostForm, CommentForm
from .models import BlogPost, Comment


class CommunityFeedTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="author",
            password="secure-test-pass-123",
        )
        cls.other_user = User.objects.create_user(
            username="reader",
            password="secure-test-pass-123",
        )
        cls.anime = Anime.objects.create(title="Paper Comet", total_episodes=10)
        cls.post = BlogPost.objects.create(
            author=cls.author,
            anime=cls.anime,
            content="The soundtrack made the finale unforgettable.",
        )

    def test_feed_shows_newest_posts_and_related_anime(self):
        response = self.client.get(reverse("social:post_list"))
        self.assertContains(response, "The soundtrack made the finale unforgettable.")
        self.assertContains(response, "Paper Comet")
        self.assertContains(response, reverse("social:post_detail", args=[self.post.pk]))

    def test_footer_shows_anime_effect_social_links(self):
        response = self.client.get(reverse("social:post_list"))
        for platform, url in [
            ("Instagram", "https://www.instagram.com/theanimeeffect/"),
            ("YouTube", "https://www.youtube.com/@theanimeeffect"),
            ("X", "https://x.com/theanimeeffect"),
            ("TikTok", "https://www.tiktok.com/@theanimeeffect"),
        ]:
            with self.subTest(platform=platform):
                self.assertContains(response, f'aria-label="{platform}"')
                self.assertContains(response, f'href="{url}"')
        self.assertContains(response, "bi bi-instagram")
        self.assertContains(response, 'rel="noopener noreferrer"')

    def test_post_detail_shows_post_and_comments(self):
        Comment.objects.create(
            post=self.post,
            author=self.other_user,
            content="I loved that ending too.",
        )
        response = self.client.get(reverse("social:post_detail", args=[self.post.pk]))
        self.assertContains(response, self.post.content)
        self.assertContains(response, "I loved that ending too.")
        self.assertContains(response, "Log in to comment")

    def test_signed_in_user_can_comment_on_a_post(self):
        self.client.force_login(self.other_user)
        response = self.client.post(
            reverse("social:post_detail", args=[self.post.pk]),
            {"content": "I loved that ending too."},
            follow=True,
        )
        self.assertContains(response, "Your comment was added.")
        self.assertContains(response, "I loved that ending too.")
        comment = Comment.objects.get(post=self.post)
        self.assertEqual(comment.author, self.other_user)

    def test_anonymous_user_is_redirected_to_login_to_comment(self):
        response = self.client.post(
            reverse("social:post_detail", args=[self.post.pk]),
            {"content": "I loved that ending too."},
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('social:post_detail', args=[self.post.pk])}",
        )
        self.assertFalse(Comment.objects.filter(post=self.post).exists())

    def test_comment_length_is_validated(self):
        form = CommentForm({"content": "x" * (Comment.MAX_CONTENT_LENGTH + 1)})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_users_can_only_edit_or_delete_their_own_posts(self):
        self.client.force_login(self.other_user)
        edit_response = self.client.get(reverse("social:post_edit", args=[self.post.pk]))
        delete_response = self.client.get(reverse("social:post_delete", args=[self.post.pk]))
        self.assertEqual(edit_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
        self.assertTrue(BlogPost.objects.filter(pk=self.post.pk).exists())

    def test_post_length_is_validated(self):
        form = BlogPostForm({"content": "x" * (BlogPost.MAX_CONTENT_LENGTH + 1), "anime": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_signed_in_user_can_publish_post(self):
        self.client.force_login(self.other_user)
        response = self.client.post(
            reverse("social:post_create"),
            {"content": "A great place to start watching.", "anime": self.anime.pk},
            follow=True,
        )
        self.assertContains(response, "Your post was published.")
        self.assertTrue(
            BlogPost.objects.filter(author=self.other_user, anime=self.anime).exists()
        )

    def test_author_can_edit_and_delete_their_post(self):
        self.client.force_login(self.author)
        edit_response = self.client.post(
            reverse("social:post_edit", args=[self.post.pk]),
            {"content": "Updated review.", "anime": self.anime.pk},
        )
        self.assertEqual(edit_response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, "Updated review.")

        delete_response = self.client.post(
            reverse("social:post_delete", args=[self.post.pk])
        )
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(BlogPost.objects.filter(pk=self.post.pk).exists())
