from django.test import TestCase
from django.urls import reverse

from accounts.tests.factories import UserFactory


class ProfilePageViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            username="testuser"
        )

        cls.profile = cls.user.profile

        cls.profile.bio = "I love cooking."
        cls.profile.save()

    def test_profile_page_returns_200(self):

        response = self.client.get(
            reverse(
                "show_profile_page",
                kwargs={
                    "pk": self.profile.pk
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_profile_page_uses_correct_template(self):

        response = self.client.get(
            reverse(
                "show_profile_page",
                kwargs={
                    "pk": self.profile.pk
                }
            )
        )

        self.assertTemplateUsed(
            response,
            "registration/user_profile.html"
        )

    def test_profile_bio_is_displayed(self):

        response = self.client.get(
            reverse(
                "show_profile_page",
                kwargs={
                    "pk": self.profile.pk
                }
            )
        )

        self.assertContains(
            response,
            "I love cooking."
        )

    def test_nonexistent_user_returns_404(self):

        response = self.client.get(
            reverse(
                "show_profile_page",
                kwargs={
                    "pk": 0
                }
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )


class EditAccountViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(
            username="testuser"
        )
        

    def test_anonymous_user_cannot_access_edit_page(self):
        edit_url = reverse(
            "edit_profile_page",
            kwargs={"pk": self.user.profile.pk}
        )

        response = self.client.get(edit_url)

        login_url = reverse("login")
        self.assertRedirects(
            response,
            f"{login_url}?next={edit_url}"
        )

        self.assertEqual(
            response.status_code,
            302
        )
        self.assertIn(
            "/accounts/login/",
            response.url
        )

    def test_authenticated_user_can_access_edit_page(self):

        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "edit_profile_page",
                kwargs={
                    "pk": self.user.profile.pk
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_edit_page_uses_correct_template(self):

        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "edit_profile_page",
                kwargs={
                    "pk": self.user.profile.pk
                }
            )
        )

        self.assertTemplateUsed(
            response,
            "registration/edit_profile_page.html"
        )

    def test_user_can_update_account(self):

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("edit_account",
                    kwargs={
                        "pk": self.user.profile.pk
                    }
                ),
            {
                "username": "newusername",
                "email": "new@example.com",
                
            }
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.username,
            "newusername"
        )

        self.assertEqual(
            self.user.email,
            "new@example.com"
        )

        self.assertEqual(
            response.status_code,
            302
        )