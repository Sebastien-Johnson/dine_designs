from django.test import TestCase

from accounts.models import CustomUser, Profile
from accounts.tests.factories import UserFactory


class CustomUserModelTest(TestCase):

    def test_user_is_created(self):

        user = UserFactory(
            username="testuser"
        )

        self.assertEqual(
            CustomUser.objects.count(),
            1
        )

    def test_user_string_representation(self):

        user = UserFactory(
            username="testuser"
        )

        self.assertEqual(
            str(user),
            "testuser"
        )

    def test_password_is_hashed(self):

        user = UserFactory()

        self.assertNotEqual(
            user.password,
            "testpass123"
        )

        self.assertTrue(
            user.check_password("testpass123")
        )


class ProfileModelTest(TestCase):

    def test_profile_is_automatically_created(self):

        user = UserFactory()

        self.assertEqual(
            Profile.objects.filter(user=user).count(),
            1
        )

    def test_profile_is_connected_to_user(self):

        user = UserFactory()

        profile = user.profile

        self.assertEqual(
            profile.user,
            user
        )

    def test_profile_string_representation(self):

        user = UserFactory(
            username="testuser"
        )

        profile = user.profile

        self.assertEqual(
            str(profile),
            "testuser"
        )

class ProfileSignalTest(TestCase):

    def test_profile_is_created_when_user_is_created(self):

        user = UserFactory()

        self.assertTrue(
            Profile.objects.filter(user=user).exists()
        )