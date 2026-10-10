from django.test import TestCase

from accounts.models import CustomUser
from recipes.models import Recipe


class RecipeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        cls.recipe = Recipe.objects.create(
            title="Test Pasta",
            author=cls.user,
            instructions="Boil pasta.",
            cooking_time=20,
            serves=4,
        )

    def test_recipe_is_created(self):
        self.assertEqual(Recipe.objects.count(), 1)

    def test_recipe_title(self):
        self.assertEqual(self.recipe.title, "Test Pasta")

    def test_recipe_author(self):
        self.assertEqual(self.recipe.author, self.user)

    def test_recipe_string_representation(self):
        self.assertEqual(str(self.recipe), "Test Pasta")

    def test_recipe_instructions(self):
        self.assertEqual(
            self.recipe.instructions,
            "Boil pasta."
        )

    def test_recipe_cooking_time(self):
        self.assertEqual(self.recipe.cooking_time, 20)

    def test_recipe_serves(self):
        self.assertEqual(self.recipe.serves, 4)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.recipe.get_absolute_url(),
            f"/{self.recipe.pk}/"
        )