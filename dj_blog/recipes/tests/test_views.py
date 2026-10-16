from datetime import date
from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe, Ingredient, Rating, Comment
from recipes.tests.factories import *


class RecipeListViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.recipe = RecipeFactory(title="Chicken Soup")

    def test_recipe_list_returns_200(self):
        response = self.client.get(reverse("recipe_list"))

        self.assertEqual(response.status_code, 200)

    def test_recipe_list_displays_recipes(self):
        response = self.client.get(reverse("recipe_list"))

        self.assertContains(response, "Chicken Soup")

    def test_recipe_list_orders_by_publish_date(self):
        older = RecipeFactory(published=date(2025, 1, 1))
        newer = RecipeFactory(published=date(2026, 1, 1))

        response = self.client.get(reverse("recipe_list"))
        recipes = list(response.context["object_list"])

        self.assertLess(
            recipes.index(newer),
            recipes.index(older),
        )


class RecipeDetailViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.recipe = RecipeFactory(
            author=self.user,
            title="Roast Chicken",
        )

    def test_recipe_detail_returns_200(self):
        response = self.client.get(
            reverse("recipe_detail", args=[self.recipe.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Roast Chicken")

    def test_recipe_detail_shows_instructions(self):
        InstructionFactory(
            recipe=self.recipe,
            step_number=1,
            text="Preheat the oven",
        )

        response = self.client.get(
            reverse("recipe_detail", args=[self.recipe.pk])
        )

        self.assertContains(response, "Preheat the oven")

    def test_authenticated_user_gets_their_rating_in_context(self):
        self.client.force_login(self.user)

        rating = RatingFactory(
            recipe=self.recipe,
            user=self.user,
            score=4,
        )

        response = self.client.get(
            reverse("recipe_detail", args=[self.recipe.pk])
        )

        self.assertEqual(response.context["user_rating"], rating)

    def test_anonymous_user_has_no_user_rating(self):
        response = self.client.get(
            reverse("recipe_detail", args=[self.recipe.pk])
        )

        self.assertIsNone(response.context["user_rating"])


class RecipeCreateViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)

    def test_recipe_create_page_returns_200(self):
        response = self.client.get(reverse("recipe_create"))

        self.assertEqual(response.status_code, 200)

    def test_user_can_create_recipe_with_instructions_and_ingredients(self):
        food = FoodFactory(
            base_serving=100,
            base_unit="g",
        )

        response = self.client.post(
            reverse("recipe_create"),
            {
                "title": "Test Recipe",
                "published": "2026-10-13",
                "serves": 4,
                "cooking_hours": 1,
                "cooking_minutes": 30,
                "foods": [str(food.pk)],
                f"serving_size_{food.pk}": "200",
                "instruction": [
                    "Prepare the ingredients",
                    "Cook until done",
                ],
            },
        )

        self.assertEqual(response.status_code, 302)

        recipe = Recipe.objects.get(title="Test Recipe")

        self.assertEqual(recipe.author, self.user)
        self.assertEqual(recipe.serves, 4)
        self.assertEqual(
            recipe.cooking_time.total_seconds(),
            5400,
        )

        ingredient = Ingredient.objects.get(
            recipe=recipe,
            food=food,
        )
        self.assertEqual(ingredient.serving_size, 200)

        instructions = list(
            recipe.instructions.order_by("step_number")
        )

        self.assertEqual(len(instructions), 2)
        self.assertEqual(
            instructions[0].text,
            "Prepare the ingredients",
        )
        self.assertEqual(
            instructions[1].step_number,
            2,
        )


class RecipeEditViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.recipe = RecipeFactory(author=self.user)

    def test_owner_can_open_edit_page(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("recipe_edit", args=[self.recipe.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_open_edit_page(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse("recipe_edit", args=[self.recipe.pk])
        )

        # This test documents a permission requirement.
        # It will fail until ownership is enforced in the view.
        self.assertIn(response.status_code, [403, 404])

    def test_edit_updates_existing_ingredient_serving_size(self):
        self.client.force_login(self.user)

        food = FoodFactory(base_serving=100, base_unit="g")
        ingredient = IngredientFactory(
            recipe=self.recipe,
            food=food,
            serving_size=100,
        )

        response = self.client.post(
            reverse("recipe_edit", args=[self.recipe.pk]),
            {
                "title": "Updated Recipe",
                "published": self.recipe.published.isoformat(),
                "serves": 4,
                "cooking_hours": 0,
                "cooking_minutes": 30,
                "foods": [str(food.pk)],
                f"serving_size_{food.pk}": "250",
            },
        )

        self.assertEqual(response.status_code, 302)

        ingredient.refresh_from_db()
        self.recipe.refresh_from_db()

        self.assertEqual(self.recipe.title, "Updated Recipe")
        self.assertEqual(ingredient.serving_size, 250)


class RecipeDeleteViewTests(TestCase):
    def test_delete_post_removes_recipe(self):
        user = UserFactory()
        recipe = RecipeFactory(author=user)
        self.client.force_login(user)

        response = self.client.post(
            reverse("recipe_confirm_delete", args=[recipe.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Recipe.objects.filter(pk=recipe.pk).exists()
        )


class RatingViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.recipe = RecipeFactory()
        self.client.force_login(self.user)

    def test_user_can_create_rating(self):
        response = self.client.post(
            reverse("recipe_rating", args=[self.recipe.pk]),
            {"score": 5},
        )

        self.assertEqual(response.status_code, 302)

        rating = Rating.objects.get(
            recipe=self.recipe,
            user=self.user,
        )
        self.assertEqual(rating.score, 5)

    def test_user_can_update_their_rating(self):
        rating = RatingFactory(
            recipe=self.recipe,
            user=self.user,
            score=2,
        )

        response = self.client.post(
            reverse("rating_update", args=[rating.pk]),
            {"score": 5},
        )

        self.assertEqual(response.status_code, 302)

        rating.refresh_from_db()
        self.assertEqual(rating.score, 5)

        self.assertEqual(
            Rating.objects.filter(
                recipe=self.recipe,
                user=self.user,
            ).count(),
            1,
        )

    def test_user_cannot_update_another_users_rating(self):
        other_user = UserFactory()
        rating = RatingFactory(
            recipe=self.recipe,
            user=other_user,
            score=3,
        )

        response = self.client.post(
            reverse("rating_update", args=[rating.pk]),
            {"score": 5},
        )

        self.assertEqual(response.status_code, 404)

        rating.refresh_from_db()
        self.assertEqual(rating.score, 3)


class CommentViewTests(TestCase):
    def test_comment_factory_creates_comment(self):
        comment = CommentFactory()

        self.assertTrue(
            Comment.objects.filter(pk=comment.pk).exists()
        )
        self.assertEqual(comment.recipe.comments.count(), 1)