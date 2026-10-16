from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from recipes.models import Food, Recipe, Ingredient


class RecipeSearchViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="searchuser",
            password="test-password-123",
        )

        self.chicken = Food.objects.create(
            name="Chicken breast",
        )
        self.rice = Food.objects.create(
            name="Brown rice",
        )

        self.chicken_recipe = Recipe.objects.create(
            title="Grilled Chicken",
            author=self.user,
        )
        self.rice_recipe = Recipe.objects.create(
            title="Rice Bowl",
            author=self.user,
        )

        Ingredient.objects.create(
            recipe=self.chicken_recipe,
            food=self.chicken,
        )
        Ingredient.objects.create(
            recipe=self.rice_recipe,
            food=self.rice,
        )

        self.url = reverse("recipe_search")

    def test_search_by_recipe_title(self):
        response = self.client.get(
            self.url, {"q": "Grilled"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grilled Chicken")
        self.assertNotContains(response, "Rice Bowl")

    def test_search_by_ingredient_name(self):
        response = self.client.get(
            self.url, {"q": "Chicken breast"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grilled Chicken")
        self.assertNotContains(response, "Rice Bowl")

    def test_search_is_case_insensitive(self):
        response = self.client.get(
            self.url, {"q": "GRILLED"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Grilled Chicken")

    def test_search_returns_empty_results_for_no_match(self):
        response = self.client.get(
            self.url, {"q": "NonexistentRecipe"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Grilled Chicken")
        self.assertNotContains(response, "Rice Bowl")

    def test_search_does_not_duplicate_recipes(self):
        # A recipe matching multiple ingredients should
        # still appear only once in the results.
        Food.objects.create(
            name="Chicken seasoning",
        )

        seasoning = Food.objects.get(
            name="Chicken seasoning"
        )

        Ingredient.objects.create(
            recipe=self.chicken_recipe,
            food=seasoning,
        )

        response = self.client.get(
            self.url, {"q": "Chicken"}
        )

        self.assertEqual(response.status_code, 200)

        results = response.context["recipes"]

        self.assertEqual(
            results.filter(pk=self.chicken_recipe.pk).count(),
            1,
        )

    def test_search_uses_results_partial(self):
        response = self.client.get(
            self.url, {"q": "Chicken"}
        )

        self.assertTemplateUsed(
            response,
            "partials/recipe_search_results.html",
        )

    
    def test_search_page_contains_htmx_configuration(self):
        response = self.client.get(reverse("recipe_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'hx-trigger="keyup changed delay:500ms"',
        )
        self.assertContains(
            response,
            'hx-target="#recipe-search-results"',
        )
        self.assertContains(
            response,
            'name="q"',
        )